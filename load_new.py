import pandas as pd
import json
df = pd.read_parquet("21990287/train.parquet")
print(df.head())
print(df.columns)

for index, x in df.iterrows():
    source_code = x["source_code"]
    vuln = x["oyente"]
    vuln = json.loads(vuln)
    print(x["overlapping"])
    for y in vuln:
        name = y["error"]
        line = y["line"]
        print(source_code.splitlines()[line - 1])
    print(vuln)