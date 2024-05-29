from datasets import load_dataset
import json
import os
import re
from transformers import AutoTokenizer


os.environ['HF_TOKEN'] = "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"
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

json_todump = list()
# Load dataset
dataset = load_dataset("AlfredPros/smart-contracts-instructions", split="train")
cont = 0
for x in dataset:
    cont += 1
    if cont == 800:
        break

    messages = [
        {"role": "system",
         "content": "You are a smart contract generator for Ethereum blockchain. You receive instruction for the generation of a smart contract and generate the source code in Solidity."},
        {"role": "user", "content": x['instruction']},
        {"role": "assistant", "content": x['source_code']},
    ]
    tosend = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    json_todump.append(
        {
            "text": tosend})

toprint_dataset = list()
with open('vulnerabilities.json') as fp:
    all_vuln = json.load(fp)
    for vuln_items in all_vuln:
        toprint_rel_dataset = dict()
        question = "Can you check if the following smart contract written in Solidity contains a vulnerability? "
        look_at = vuln_items['path']
        indexes = ""
        vulns_line = ""
        cat = ""
        for row_vuln in vuln_items['vulnerabilities']:
            fp_vuln = open(look_at)
            cat = row_vuln['category']
            all_lines = ""

            for i, line in enumerate(fp_vuln):
                j = i + 1
                line = re.sub(r'\/\/.*', '', line)
                line = re.sub(r'\/\*.*?\*\/', '', line, flags=re.DOTALL)
                if line.startswith("/*") or line.startswith(" *") or line.startswith("  *") or line.startswith(" */") or line == r"\n" or line == "":
                    continue
                ar_par_split = line.split("{")
                for x in range(0, len(ar_par_split)):
                    ar_par_split[x] = ar_par_split[x].strip()
                if len(ar_par_split) > 1:
                    line = "{".join(ar_par_split)
                all_lines += line.strip().split("//")[0].strip().replace("\n", "") + r"\n "
                if j in row_vuln['lines']:
                    indexes += str(i) + ", "
                    vulns_line += line.split("//")[0].strip() + r"\n "
        indexes = indexes[:-2]
        question += all_lines
        toprint_rel_dataset['sc_name'] = look_at
        toprint_rel_dataset['question_1'] = question
        toprint_rel_dataset['answer_1'] = "Yes, it contains a vulnerability."
        toprint_rel_dataset[
            'question_2'] = "Can you tell me which is the vulnerability and which is the line of code associated with it?"
        toadd = "Yes, of couse. The vulnerability is classified as " + cat.title().replace("_",
                                                                                           " ") + " due to these instructions " + vulns_line
        toprint_rel_dataset['answer_2'] = toadd
        toprint_dataset.append(toprint_rel_dataset)
        toprint_rel_dataset['question_sug'] = "Can you suggest me how to mitigate this vulnerability?"
        if cat == "access_control":
            toprint_rel_dataset[
                'answer_sug'] = "An access control vulnerability in a Solidity smart contract is a type of security flaw that lets unauthorized users access or modify the contract’s data or functions. I suggest you to revise the line " + vulns_line + " by improving the access control mechanism"
        else:
            toprint_rel_dataset['answer_sug'] = "Apply some method to prevent " + cat.title().replace("_", " ")

for x in toprint_dataset:
    messages = [
        {"role": "system",
         "content": "You are a smart contract security analyzer called VulnHunt. You receive smart contract written in Solidity as input and answer with the vulnearbility identified if exist. You can also offer remediations to vulnerabilities found, only if the user ask you."},
        {"role": "user", "content": x['question_1']},
        {"role": "assistant", "content": x['answer_1']},
        {"role": "user", "content": x['question_2']},
        {"role": "assistant", "content": x['answer_2']},
        {"role": "user", "content": x['question_sug']},
        {"role": "assistant", "content": x['answer_sug']},
    ]
    tosend = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    print(tosend)
    json_todump.append(
        {
            "text": tosend})
fp_write = open("export.json", "w+")
json.dump(json_todump, fp_write)
fp_write.close()

