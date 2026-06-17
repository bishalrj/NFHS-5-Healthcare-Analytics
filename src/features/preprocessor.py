import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class HealthcareDataPreprocessor:
    """
    Production-grade data preprocessing pipeline for district-level healthcare data.
    """
    def __init__(self, missing_threshold: float = 0.15):
        self.missing_threshold = missing_threshold
        self.imputer = SimpleImputer(strategy='median')
        self.dropped_features_ = []
        self.selected_features_ = [
            "Population below age 15 years (%)",
            "Sex ratio at birth for children born in the last five years (females per 1,000 males)",
            "Female population age 6 years and above who ever attended school (%)",
            "Women age 20-24 years married before age 18 years (%)",
            "Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Any modern method6 (%)",
            "Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)",
            "Institutional births (in the 5 years before the survey) (%)",
            "Children age 12-23 months fully vaccinated based on information from either vaccination card or mother's recall11 (%)",
            "Prevalence of diarrhoea in the 2 weeks preceding the survey (Children under age 5 years) (%) ",
            "Children under 5 years who are stunted (height-for-age)18 (%)",
            "Women (age 15-49 years) whose Body Mass Index (BMI) is below normal (BMI <18.5 kg/m2)21 (%)",
            "All women age 15-49 years who are anaemic22 (%)",
            "Population living in households that use an improved sanitation facility2 (%)",
            "Households using clean fuel for cooking3 (%)",
            "Women age 15 years and above wih Elevated blood pressure (Systolic >=140 mm of Hg and/or Diastolic >=90 mm of Hg) or taking medicine to control blood pressure (%)",
            "Men age 15 years and above who use any kind of tobacco (%)",
            "Households with any usual member covered under a health insurance/financing scheme (%)",
            "Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)"
        ]

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the cleaning pipeline:
        1. Drops columns exceeding the missing value threshold.
        2. Filters out highly correlated/redundant features automatically or by manually selecting domain representatives.
        3. Applies median imputation.
        4. Handles outliers via Winsorization (1st and 99th percentile capping).
        """
        df_clean = df.copy()
        
        # 1. Feature Removal Threshold
        missing_frac = df_clean.isnull().mean()
        self.dropped_features_ = missing_frac[missing_frac > self.missing_threshold].index.tolist()
        df_clean.drop(columns=self.dropped_features_, inplace=True, errors='ignore')
        
        # We also need to keep identifiers
        identifiers = ['District Names', 'State/UT']
        
        # Keep only the selected features + identifiers if they exist in df_clean
        final_cols = identifiers + [col for col in self.selected_features_ if col in df_clean.columns]
        
        # Optional: check if we dropped any selected feature due to missing threshold
        # (Average out-of-pocket might be one, but its missingness is low)
        
        df_selected = df_clean[final_cols].copy()
        
        numeric_cols = df_selected.select_dtypes(include=[np.number]).columns.tolist()
        
        # 2. Median Imputation
        df_selected[numeric_cols] = self.imputer.fit_transform(df_selected[numeric_cols])
        
        # 3. Outlier Handling (Winsorization)
        for col in numeric_cols:
            lower_bound = df_selected[col].quantile(0.01)
            upper_bound = df_selected[col].quantile(0.99)
            df_selected[col] = np.clip(df_selected[col], lower_bound, upper_bound)
            
        return df_selected
