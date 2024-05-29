import json

toprint_dataset = list()
json_todump = list()
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
                if line.startswith("/*") or line.startswith(" *") or line.startswith(" */"):
                    continue
                all_lines += line
                if j in row_vuln['lines']:
                    indexes += str(i) + ", "
                    vulns_line += line + " "
        indexes = indexes[:-2]
        question += all_lines + "``` ."
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
    json_todump.append(
        {
            "text": "<s> [INST] {question_1} [/INST] {answer_1} </s><s> [INST] {question_2} [/INST] {answer_2} </s><s> [INST] {question_sug} [/INST] {answer_sug} </s> }}".format(
                question_1=x['question_1'], answer_1=x['answer_1'], question_2=x['question_2'], answer_2=x['answer_2'],
                question_sug=x['question_sug'], answer_sug=x['answer_sug'])})
fp_write = open("export.json", "w+")
print(json.dump(json_todump, fp_write))
fp_write.close()
