import json
import os
import pandas as pd
from src.data import load_and_clean_data
from src.features import HealthcareDataPreprocessor

def main():
    """
    Day 2 Pipeline: Preprocessing and Feature Selection
    """
    print("Loading data...")
    df = load_and_clean_data('data/nfhs5_district.csv')
    
    # Identify non-numeric artifacts was handled in load_and_clean_data
    # But let's log missingness before pipeline
    missing_before = df.isnull().sum()
    
    print("Running Preprocessing Pipeline...")
    preprocessor = HealthcareDataPreprocessor(missing_threshold=0.15)
    df_clean = preprocessor.fit_transform(df)
    
    # Save the model-ready dataset
    os.makedirs('data/processed', exist_ok=True)
    df_clean.to_csv('data/processed/model_ready_data.csv', index=False)
    
    # Generate Data Quality Report
    report = {
        'initial_shape': df.shape,
        'final_shape': df_clean.shape,
        'dropped_features_due_to_missingness': preprocessor.dropped_features_,
        'selected_features': [c for c in df_clean.columns if c not in ['District Names', 'State/UT']],
        'imputation_strategy': 'Median Imputation',
        'outlier_handling': 'Winsorization (1st and 99th percentile capping)'
    }
    
    os.makedirs('reports', exist_ok=True)
    with open('reports/day2_quality_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
        
    print("Day 2 Pipeline Complete.")
    print("Model-ready data saved to data/processed/model_ready_data.csv")
    print(f"Number of features selected for clustering: {len(report['selected_features'])}")

if __name__ == '__main__':
    main()
