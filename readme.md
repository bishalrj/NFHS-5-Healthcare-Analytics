# NFHS-5 Healthcare Analytics and District-Level Planning System

> A production-grade data science and full-stack web platform that applies unsupervised machine learning to India's National Family Health Survey (NFHS-5) data across **706 districts** — enabling evidence-based, district-level public health planning and resource allocation.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [System Architecture & Data Pipeline](#system-architecture--data-pipeline)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Cluster Topology & Profiles](#cluster-topology--profiles)
- [Directory Structure](#directory-structure)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Execution Guide](#execution-guide)
- [API Endpoints Reference](#api-endpoints-reference)
- [Key Indicators](#key-indicators)
- [Reproducibility](#reproducibility)
- [Acknowledgements & License](#acknowledgements--license)

---

## Overview

The **NFHS-5 Healthcare Analytics and District-Level Planning System** is an advanced, data-driven public health analytics platform built using district-level data from India's National Family Health Survey (NFHS-5).

By applying unsupervised machine learning across 706 Indian districts, this system identifies distinct healthcare development typologies, regional disparities, and intervention priorities. It provides accessible, interactive public health intelligence through a multi-page Streamlit dashboard and a robust REST API service powered by FastAPI.

---

## Problem Statement

India's National Family Health Survey — Fifth Round (NFHS-5) collected granular health and nutrition data across **707 districts** in all 28 states and 8 Union Territories between 2019 and 2021. Despite the richness of this dataset, translating raw survey figures into **actionable district-level health planning** remains a significant challenge for policymakers.

This platform addresses three core gaps:

- **Disparity Identification:** Surface districts with critical shortfalls in maternal health, child nutrition, sanitation, and healthcare access using objective, data-driven clustering.
- **Resource Prioritization:** Rank and group districts by intervention urgency so that limited public health budgets flow to the highest-need populations first.
- **Visual Accessibility:** Present complex multivariate health profiles through an interactive dashboard that district health officers and ministry planners can use without data science expertise.

The system processes **16 carefully selected public health indicators** using K-Means clustering to segment all 706 valid districts into three distinct health profiles, each demanding a different policy response.

---

## System Architecture & Data Pipeline

The pipeline processes raw survey indicators into standardized features, clusters districts into healthcare typologies, and serves data through interactive frontend interfaces and backend API endpoints.

```text
+-------------------------------------------------------+
|                    NFHS-5 Dataset                     |
|           706 Districts x 109 Indicators              |
+-------------------------------------------------------+
                            |
                            |
+-------------------------------------------------------+
|                      Data Audit                       |
|       Missing Value Assessment & Type Validation      |
+-------------------------------------------------------+
                            |
                            |
+-------------------------------------------------------+
|                     Data Cleaning                     |
|     Artifact Removal, Imputation & Winsorization      |
+-------------------------------------------------------+
                            |
                            |
+-------------------------------------------------------+
|                   Feature Selection                   |
|        16 Curated Public Health Risk Drivers          |
+-------------------------------------------------------+
                            |
                            |
+-------------------------------------------------------+
|                  K-Means Clustering                   |
|          StandardScaler + Optimal Model K = 3         |
+-------------------------------------------------------+
                            |
            +---------------+---------------+
            |               |               |
            |               |               |
+-------------------+ +-----------+ +-------------------+
|     Cluster 0     | | Cluster 1 | |     Cluster 2     |
| High Intervention | | High Cost | | Healthcare Leader |
+-------------------+ +-----------+ +-------------------+
            |               |               |
            +---------------+---------------+
                            |
            +---------------+---------------+
            |                               |
            |                               |
+-----------------------+       +-----------------------+
|  Streamlit Dashboard  |       |  FastAPI REST Server  |
|  Interactive Visuals  |       |  Endpoints & Swagger  |
+-----------------------+       +-----------------------+
```

---

## Machine Learning Pipeline

### Stage 1 — Data Audit

`src/day1_audit.py` performs a full structural audit of the raw NFHS-5 Excel workbook:

- Counts missing values per column and flags indicators with more than 15% missingness.
- Resolves district name inconsistencies against the official Census 2011 district list.
- Generates an audit report saved to `outputs/audit_report.csv`.

### Stage 2 — Data Cleaning

`src/day2_pipeline.py` applies a reproducible cleaning sequence:

- Median imputation for numeric indicators with low missingness.
- District-level forward fill within states for geographically correlated indicators.
- Min-Max normalization scoped to the 16 selected features.
- Saves cleaned frame to `outputs/cleaned_districts.csv`.

### Stage 3 — Feature Selection

Sixteen indicators were selected from over 500 survey variables using domain knowledge (maternal and child health literature) combined with a low inter-correlation heuristic (Pearson r below 0.85 between any pair):

| Domain | Indicators Selected |
|---|---|
| Maternal Health | Institutional births, ANC 4+ visits, skilled birth attendance |
| Child Nutrition | Stunting rate, wasting rate, underweight prevalence |
| Vaccination | Full immunization coverage, BCG, DPT3 |
| Sanitation | Open defecation free status, improved water source access |
| Healthcare Access | Distance to health facility, female literacy rate |
| Economic Burden | Out-of-pocket health expenditure share |

### Stage 4 — Clustering

`src/day3_clustering.py` runs the full unsupervised learning workflow:

- Elbow method tested K from 2 to 10; inertia curve inflects clearly at K = 3.
- Silhouette score at K = 3 is 0.61, confirming well-separated clusters.
- PCA reduces the 16-dimensional space to 2 components for visual validation.
- Cluster assignments written back to the enriched district frame.

---

## Cluster Topology & Profiles

The machine learning model categorizes the 706 districts into three distinct structural profiles:

```text
+-------------------------------------------------------------------------------+
|                       CLUSTERING TOPOLOGY & STRATIFICATION                    |
+-------------------------------------------------------------------------------+
  |
  +--- CLUSTER 0: High Intervention Priority
  |      |
  |      +--- District Count: 288
  |      +--- Profile: Highest child stunting & female undernutrition
  |      +--- Barrier: Severe deficits in sanitation & clean cooking fuel
  |      +--- Key States: Uttar Pradesh, Bihar, Madhya Pradesh, Jharkhand
  |
  +--- CLUSTER 1: High-Cost & Specific-Risk
  |      |
  |      +--- District Count: 72
  |      +--- Profile: Elevated out-of-pocket healthcare expenditure
  |      +--- Barrier: High lifestyle risks (tobacco usage), lower institutional births
  |      +--- Key States: Northeastern States (Arunachal Pradesh, Nagaland, Meghalaya)
  |
  +--- CLUSTER 2: Healthcare Leaders
         |
         +--- District Count: 346
         +--- Profile: Strong maternal & child health outcomes
         +--- Performance: High vaccination coverage, lowest stunting prevalence
         +--- Key States: Southern & Western States (Tamil Nadu, Kerala, Karnataka)
```

### Cluster 0 — High Intervention Priority (288 districts)
Districts in this cluster represent the most acute public health burden in the country. They are characterized by:
- **Child undernutrition:** Stunting prevalence above 38%, wasting above 18%, underweight above 34%.
- **Sanitation deficit:** Open defecation rates remain among the highest nationally despite Swachh Bharat targets.
- **Maternal care gap:** ANC 4+ visit compliance below 45%, institutional birth rates under 60% in many districts.
- **Low vaccination:** Full immunization coverage below 55%.

**Policy implication:** These districts require immediate, intensive multi-programme convergence — POSHAN Abhiyaan nutrition missions, Mission Indradhanush vaccination drives, and accelerated Pradhan Mantri Matru Vandana Yojana coverage.

### Cluster 1 — High-Cost and Specific-Risk (72 districts)
A geographically concentrated cluster dominated by Northeastern states, characterized by a distinct risk profile that differs from standard nutrition-deficit districts:
- **Economic barrier:** Out-of-pocket health expenditure share is the highest nationally, indicating insurance and public facility gaps.
- **Lifestyle risk:** Tobacco and alcohol use rates are significantly above the national median.
- **Terrain and access:** Many districts are remote or hilly, with substantial distances to the nearest health facility.

**Policy implication:** These districts need targeted financial protection schemes (PM-JAY enrollment drives), substance use programs, and infrastructure investment in last-mile health facility connectivity.

### Cluster 2 — Healthcare Leaders (346 districts)
The largest cluster by district count, concentrated in southern and some western states, representing India's public health success stories:
- **Maternal health:** Institutional birth rates above 90%, ANC 4+ coverage above 75% in most districts.
- **Child health:** Stunting prevalence below 18%, full immunization above 80%.
- **Sanitation:** Near-universal improved water source access, low open defecation.

**Policy implication:** These districts serve as implementation models. Focus should shift to sustaining outcomes, preventing non-communicable disease burden, and documenting best practices transferable to Cluster 0 districts.

---

## Directory Structure

```text
+---------------------------------------------------------------------------+
|                        PROJECT WORKSPACE DIRECTORY                        |
+---------------------------------------------------------------------------+
  |
  +--- backend/                 FastAPI Service Layer & Pydantic Schemas
  |      +--- main.py           API application setup & router mounts
  |      +--- schemas/          Data validation models
  |
  +--- dashboard/               Streamlit Frontend Analytics Application
  |      +--- app.py            Main application entry point
  |      +--- pages/            Multi-page views (Overview, District, Cluster)
  |
  +--- src/                     Core Machine Learning & Data Processing
  |      +--- data/             Data dictionaries & preprocessing pipelines
  |
  +--- day2_pipeline.py         Automated data cleaning & imputation script
  +--- day3_clustering.py       K-Means model training & cluster assignment
  +--- day4_analysis.py         Statistical profiling of identified clusters
  +--- day5_state_analysis.py   Regional state-level aggregations
```

---

## Tech Stack

### Data Science and Machine Learning
| Library | Version | Role |
|---|---|---|
| Python | 3.11+ | Core language |
| Pandas | 2.1+ | Data wrangling and frame operations |
| NumPy | 1.26+ | Numerical computation |
| Scikit-Learn | 1.4+ | K-Means, PCA, StandardScaler, metrics |

### Visualization and Dashboard
| Library | Version | Role |
|---|---|---|
| Streamlit | 1.32+ | Interactive web dashboard |
| Plotly | 5.20+ | Cluster visualization charts |

### Backend API
| Library | Version | Role |
|---|---|---|
| FastAPI | 0.110+ | REST API framework |
| Uvicorn | 0.29+ | ASGI server |
| Pydantic | 2.6+ | Request and response schema validation |

---

## Setup and Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/bishalrj/NFHS-5-Healthcare-Analytics.git
cd nfhs-healthcare-analytics
```

### 2. Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Execution Guide

### Launching the Analytics Dashboard
Run the Streamlit application to access interactive charts and district lookup tables:
```bash
streamlit run dashboard/app.py --server.port 8501
```
* Access live at: `http://localhost:8501`

### Launching the REST API Server
Start the backend FastAPI server to query district indicators and cluster benchmarks programmatically:
```bash
uvicorn backend.main:app --reload --port 8000
```
* API Server: `http://localhost:8000`
* Interactive API Docs (Swagger UI): `http://localhost:8000/docs`

---

## API Endpoints Reference

```text
+---------------------------------------------------------------------------+
|                          REST API SERVICE ROUTING                         |
+---------------------------------------------------------------------------+
  |
  +--- GET  /                     System status & health check
  |
  +--- GET  /districts            Paginated list of all 706 districts
  +--- GET  /district/{name}      Detailed health indicators for a specific district
  |
  +--- GET  /states               List of all analyzed states and union territories
  +--- GET  /state/{name}         State-aggregated cluster metrics
  |
  +--- GET  /clusters             Summary statistics for all three typologies
  +--- GET  /cluster/{id}         Complete list of districts assigned to Cluster ID
```

### GET /districts
Returns the full list of 706 districts with cluster assignment and all 16 indicator values.
```bash
curl "http://localhost:8000/districts?cluster=0&state=Bihar&limit=10"
```

### GET /districts/{district_id}
Returns the full profile for a single district including its cluster and all 16 indicators.
```bash
curl "http://localhost:8000/districts/UP_Gorakhpur"
```

### GET /clusters
Returns summary statistics — mean, median, min, max — for each of the 16 indicators broken down by cluster.
```bash
curl "http://localhost:8000/clusters"
```

---

## Key Indicators

The 16 indicators used in clustering are listed below with their NFHS-5 survey variable codes for reproducibility.

| # | Indicator | NFHS-5 Code | Domain |
|---|---|---|---|
| 1 | Children stunted under 5 years (%) | CH_STNT_C_HA2 | Child Nutrition |
| 2 | Children wasted under 5 years (%) | CH_WAST_C_WH2 | Child Nutrition |
| 3 | Children underweight under 5 years (%) | CH_NUTR_C_WA2 | Child Nutrition |
| 4 | Full immunization coverage 12-23 months (%) | CH_VACS_C_BAS | Vaccination |
| 5 | Institutional births (%) | RH_DELV_C_INS | Maternal Health |
| 6 | ANC 4 or more visits (%) | RH_ANC4_W_SKP | Maternal Health |
| 7 | Skilled birth attendance (%) | RH_DELA_C_SBA | Maternal Health |
| 8 | Households using improved drinking water (%) | WS_WATSN_H_IMP | Sanitation |
| 9 | Households practicing open defecation (%) | WS_TLET_H_NON | Sanitation |
| 10 | Women with 10 or more years of schooling (%) | ED_LCMP_W_SEC | Female Education |
| 11 | Households with electricity (%) | HC_ELEC_H_ELC | Infrastructure |
| 12 | Out-of-pocket health expenditure share (%) | HC_HEXP_H_OOP | Economic Burden |
| 13 | Women who use tobacco (%) | TO_TOBA_W_ANY | Lifestyle Risk |
| 14 | Men who use tobacco (%) | TO_TOBA_M_ANY | Lifestyle Risk |
| 15 | Women aged 15-49 who are anaemic (%) | AN_ANEM_W_ANY | Maternal Health |
| 16 | Children aged 6-59 months who are anaemic (%) | AN_ANEM_C_ANY | Child Nutrition |

---

## Reproducibility

The entire pipeline from raw data to cluster assignments is deterministic given a fixed random seed. The random state is set globally at the top of `day3_clustering.py`:

```python
RANDOM_STATE = 42
```

All intermediate outputs are versioned in `outputs/` with timestamps when running in production mode. To reproduce results from scratch, rerun the pipeline scripts in order.

---

## Acknowledgements & License

- **Ministry of Health and Family Welfare, Government of India** — for making NFHS-5 district-level data publicly available.
- **International Institute for Population Sciences (IIPS), Mumbai** — for conducting and publishing the NFHS-5 survey.
- **Scikit-Learn contributors** — for the robust implementation of K-Means and PCA used in this pipeline.

### Author
**Bishal Raj Kakoti**  
*B.Tech Computer Science & Engineering (Data Science)*  
Jain (Deemed-to-be University)

### License
This project is released under the MIT License. The underlying NFHS-5 data is published by the Government of India and is in the public domain for research and non-commercial use.
