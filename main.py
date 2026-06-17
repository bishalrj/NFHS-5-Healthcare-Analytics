import json
import os
from src.data import load_and_clean_data, DataAuditor, get_healthcare_data_dictionary

def main():
    """
    Main entrypoint for the Day-1 Data Audit of NFHS-5 dataset.
    """
    data_path = 'data/nfhs5_district.csv'
    
    print("Loading and cleaning data...")
    df = load_and_clean_data(data_path)
    
    print("Performing data audit...")
    auditor = DataAuditor(df)
    audit_results = auditor.generate_audit()
    
    print("Saving audit results to reports/audit_results.json...")
    os.makedirs('reports', exist_ok=True)
    with open('reports/audit_results.json', 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=4)
        
    print("Audit Complete. You can view the results in reports/audit_results.json")
    
if __name__ == '__main__':
    main()
