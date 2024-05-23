import json

toprint_dataset = list()
json_todump = list()
with open('vulnerabilities.json') as fp:
    all_vuln = json.load(fp)
    for vuln_items in all_vuln:
        toprint_rel_dataset = dict()
        question = "Find the vulnerability in the following smart contract ```"
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
        toprint_rel_dataset['question'] = question
        toadd = "Vulnerability detected, it is classified as " + cat.title().replace("_",
                                                                                     " ") + " due to these instructions ```" + vulns_line + "```"
        toprint_rel_dataset['answer'] = toadd
        toprint_dataset.append(toprint_rel_dataset)
        toprint_rel_dataset['question_sug'] = "How can this vulnerability be mitigated?"
for x in toprint_dataset:
    json_todump.append(
        {"text": "<s> [INST] {question} [/INST] {answer} </s>}}".format(question=x['question'], answer=x['answer'])})
fp_write = open("export.json", "w+")
print(json.dump(json_todump, fp_write))
fp_write.close()
