import pandas as pd
from typing import Tuple

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """
    Loads the NFHS-5 dataset and performs initial data type cleaning.
    Converts string-represented numeric columns back to float/int after 
    stripping specific characters like parentheses and asterisks used to 
    denote missing or suppressed data.
    """
    df = pd.read_csv(filepath)
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        if df[col].dtype == 'object' and col not in ['District Names', 'State/UT']:
            # Remove symbols that prevent numeric casting
            cleaned = df[col].astype(str).str.replace('(', '', regex=False)\
                                         .str.replace(')', '', regex=False)\
                                         .str.replace('*', '', regex=False)\
                                         .str.strip()
            # Convert to numeric, errors='coerce' will turn 'na' and remaining strings to NaN
            df[col] = pd.to_numeric(cleaned, errors='coerce')
            
    return df
