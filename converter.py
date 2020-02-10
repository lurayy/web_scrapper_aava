import pandas as pd 

with open('data/output_json.json', 'r') as f_input:
    df = pd.read_json(f_input)

df.to_csv('data/output_csv.csv', index=False)