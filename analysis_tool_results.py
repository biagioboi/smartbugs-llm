import pandas as pd
import json


def mapping_vuln(tool_name, vulnerabilities, kind):
    if tool_name == "osiris":
        if ("Overflow_bugs" or "Underflow_bugs" in vulnerabilities) and kind == "integeroverflow(OF)":
            return ["Integer_Arithmetic_Bugs_SWC_101"]
        if ("Reentrancy_bug" in vulnerabilities) and kind == "reentrancy(RE)":
            return ["External_Call_To_User_Supplied_Address_SWC_107"]
        if ("Time_dependency_bug" in vulnerabilities) and kind == "timestampdependency(TP)":
            return ["Dependence_on_predictable_environment_variable_SWC_116"]
    elif tool_name == "oyente":
        if ("Integer_Overflow" or "Integer_Underflow" in vulnerabilities) and kind == "integeroverflow(OF)":
            return ["Integer_Arithmetic_Bugs_SWC_101"]
        if ("Re_Entrancy_Vulnerability" in vulnerabilities) and kind == "reentrancy(RE)":
            return ["External_Call_To_User_Supplied_Address_SWC_107"]
        if ("Timestamp_Dependency" in vulnerabilities) and kind == "timestampdependency(TP)":
            return ["Dependence_on_predictable_environment_variable_SWC_116"]
    elif tool_name == "slither-0.10.0":
        if kind == "reentrancy(RE)":
            for x in vulnerabilities:
                if x.startswith("reentrancy"):
                    return ["External_Call_To_User_Supplied_Address_SWC_107"]

    return vulnerabilities

# Read the CSV file
df1 = pd.read_csv('results_tools/results_imac.csv')
df2 = pd.read_csv('results_tools/results_macbook.csv')
df3 = pd.read_csv('results_tools/results_win.csv')

# Get the category, win dataset uses a different representation for path
df3['category'] = df3.apply(lambda x: x['filename'].split("\\")[2].replace(" ", ""), axis=1)
df2['category'] = df2.apply(lambda x: x['filename'].split("/")[1].replace(" ", ""), axis=1)
df1['category'] = df1.apply(lambda x: x['filename'].split("/")[1].replace(" ", ""), axis=1)
results = pd.concat([df1, df2, df3])
tools_name = ["mythril-0.24.7", "osiris", "oyente", "maian"]

categories_name = results['category'].unique()
findings_general = list()
for cat in categories_name:
    for tool in tools_name:
        current_select = results.loc[(results['category'] == cat) & (results['toolid'] == tool)]
        if len(current_select) == 0:
            continue
        else:
            print("Analyzing {cat} with {tool}".format(cat=cat, tool=tool))
            all_findings = []
            unique_findings = dict()
            for x in current_select['findings']:
                current_findings = x[1:-1].replace(" ", "").split(",")
                filtered = mapping_vuln(tool, current_findings, cat)
                for z in filtered:
                    if z == "":
                        z = "empty"
                    if z not in unique_findings:
                        unique_findings[z] = 1
                    else:
                        unique_findings[z] += 1
            findings_general.append({"tool_name": tool, "category": cat, "findings": unique_findings})

for x in findings_general:
    print(x["category"], x["tool_name"], x["findings"])
