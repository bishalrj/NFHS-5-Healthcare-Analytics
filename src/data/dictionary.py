from typing import Dict, List

def get_healthcare_data_dictionary() -> Dict[str, List[str]]:
    """
    Returns the classification of NFHS-5 indicators into core healthcare domains.
    """
    return {
        "Demographics": [
            "Population below age 15 years (%)",
            "Sex ratio of the total population (females per 1,000 males)",
            "Sex ratio at birth for children born in the last five years (females per 1,000 males)",
            "Children under age 5 years whose birth was registered with the civil authority (%)",
            "Deaths in the last 3 years registered with the civil authority (%)",
            "Women age 20-24 years married before age 18 years (%)"
        ],
        "Education": [
            "Female population age 6 years and above who ever attended school (%)",
            "Children age 5 years who attended pre-primary school during the school year 2019-20 (%)",
            "Women (age 15-49) who are literate4 (%)",
            "Women (age 15-49)  with 10 or more years of schooling (%)"
        ],
        "Maternal Health": [
            "Mothers who had an antenatal check-up in the first trimester  (for last birth in the 5 years before the survey) (%)",
            "Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)",
            "Mothers who consumed iron folic acid for 100 days or more when they were pregnant (for last birth in the 5 years before the survey) (%)",
            "Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (for last birth in the 5 years before the survey) (%)",
            "Institutional births (in the 5 years before the survey) (%)",
            "Births attended by skilled health personnel (in the 5 years before the survey)10 (%)",
            "Births delivered by caesarean section (in the 5 years before the survey) (%)",
            "Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Any modern method6 (%)",
            "Total Unmet need for Family Planning (Currently Married Women Age 15-49  years)7 (%)"
        ],
        "Child Health": [
            "Children age 12-23 months fully vaccinated based on information from either vaccination card or mother's recall11 (%)",
            "Children age 12-23 months who have received 3 doses of polio vaccine13 (%)",
            "Children age 12-23 months who have received 3 doses of penta or DPT vaccine (%)",
            "Prevalence of diarrhoea in the 2 weeks preceding the survey (Children under age 5 years) (%)",
            "Children Prevalence of symptoms of acute respiratory infection (ARI) in the 2 weeks preceding the survey (Children under age 5 years) (%)"
        ],
        "Nutrition": [
            "Children under age 6 months exclusively breastfed16 (%)",
            "Children under 5 years who are stunted (height-for-age)18 (%)",
            "Children under 5 years who are wasted (weight-for-height)18 (%)",
            "Children under 5 years who are underweight (weight-for-age)18 (%)",
            "Women (age 15-49 years) whose Body Mass Index (BMI) is below normal (BMI <18.5 kg/m2)21 (%)",
            "Women (age 15-49 years) who are overweight or obese (BMI >=25.0 kg/m2)21 (%)",
            "Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)",
            "All women age 15-49 years who are anaemic22 (%)"
        ],
        "Sanitation": [
            "Population living in households with an improved drinking-water source1 (%)",
            "Population living in households that use an improved sanitation facility2 (%)",
            "Households using clean fuel for cooking3 (%)",
            "Households using iodized salt (%)",
            "Women age 15-24 years who use hygienic methods of protection during their menstrual period5 (%)"
        ],
        "Lifestyle Risk Factors": [
            "Women age 15 years and above wih Elevated blood pressure (Systolic >=140 mm of Hg and/or Diastolic >=90 mm of Hg) or taking medicine to control blood pressure (%)",
            "Men age 15 years and above wih Elevated blood pressure (Systolic >=140 mm of Hg and/or Diastolic >=90 mm of Hg) or taking medicine to control blood pressure (%)",
            "Women age 15 years and above wih high or very high (>140 mg/dl) Blood sugar level or taking medicine to control blood sugar level23 (%)",
            "Men age 15 years and above wih high or very high (>140 mg/dl) Blood sugar level  or taking medicine to control blood sugar level23 (%)",
            "Women age 15 years and above who use any kind of tobacco (%)",
            "Men age 15 years and above who use any kind of tobacco (%)",
            "Women age 15 years and above who consume alcohol (%)",
            "Men age 15 years and above who consume alcohol (%)"
        ],
        "Healthcare Access": [
            "Households with any usual member covered under a health insurance/financing scheme (%)",
            "Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)",
            "Health worker ever talked to female non-users about family planning (%)",
            "Women (age 30-49 years) Ever undergone a screening test for cervical cancer (%)"
        ]
    }
