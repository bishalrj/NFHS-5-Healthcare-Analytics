import pandas as pd
import json
import numpy as np

df = pd.read_csv('data/nfhs5_district.csv')

# Clean columns: remove parentheses and asterisks
for col in df.columns:
    if df[col].dtype == 'object' and col not in ['District Names', 'State/UT']:
        # Remove parentheses and asterisks
        cleaned = df[col].astype(str).str.replace('(', '', regex=False).str.replace(')', '', regex=False).str.replace('*', '', regex=False).str.strip()
        # Replace non-numeric with NaN where appropriate, though we can just use pd.to_numeric
        df[col] = pd.to_numeric(cleaned, errors='coerce')

audit_results = {
    'columns': df.columns.tolist(),
    'num_rows': len(df),
    'num_cols': len(df.columns),
    'dtypes': df.dtypes.astype(str).to_dict(),
    'missing_values': df.isnull().sum().to_dict(),
    'duplicates': int(df.duplicated().sum()),
    'constant_columns': [col for col in df.columns if df[col].nunique(dropna=True) <= 1],
    'high_cardinality_columns': [col for col in df.columns if df[col].nunique(dropna=True) > 0.9 * len(df)]
}

with open('audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, indent=4)
