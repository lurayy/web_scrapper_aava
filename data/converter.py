import pandas as pd 

with open('output_json.json', 'r') as f_input:
    df = pd.read_json(f_input)

df.to_csv('output.csv', index=False)