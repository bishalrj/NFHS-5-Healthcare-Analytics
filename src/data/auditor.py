import pandas as pd
from typing import Dict, Any, List

class DataAuditor:
    """
    Performs a comprehensive day-1 data audit on the healthcare dataset.
    Follows consulting best practices to inspect shape, missingness, and cardinality.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def generate_audit(self) -> Dict[str, Any]:
        """
        Generates the full data audit report.
        """
        num_rows = len(self.df)
        num_cols = len(self.df.columns)
        
        # Categorize columns by types
        numerical_features = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Check missing values
        missing_counts = self.df.isnull().sum()
        missing_dict = missing_counts[missing_counts > 0].to_dict()
        
        # Check duplicates
        duplicates = int(self.df.duplicated().sum())
        
        # Check constant and high cardinality
        constant_columns = [col for col in self.df.columns if self.df[col].nunique(dropna=True) <= 1]
        
        # Threshold for high cardinality: unique values > 90% of rows for categorical, 
        # but for continuous numeric, this is normal. We only flag categorical/identifier high cardinality.
        high_card_columns = [
            col for col in categorical_features 
            if self.df[col].nunique(dropna=True) > 0.9 * num_rows
        ]
        
        return {
            'summary': {
                'total_rows': num_rows,
                'total_columns': num_cols,
                'duplicates': duplicates,
            },
            'feature_inventory': {
                'numerical_features_count': len(numerical_features),
                'categorical_features_count': len(categorical_features),
                'numerical_features': numerical_features,
                'categorical_features': categorical_features
            },
            'missing_values': missing_dict,
            'constant_columns': constant_columns,
            'high_cardinality_columns': high_card_columns
        }
