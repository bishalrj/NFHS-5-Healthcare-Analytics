# NFHS-5 Healthcare Analytics and District-Level Planning System

> A production-grade data science and full-stack web platform that applies unsupervised machine learning to India's National Family Health Survey (NFHS-5) data across **706 districts** — enabling evidence-based, district-level public health planning and resource allocation.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Cluster Topology and Profiles](#cluster-topology-and-profiles)
- [Directory Structure](#directory-structure)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Key Indicators](#key-indicators)
- [Acknowledgements](#acknowledgements)

---

## Problem Statement

India's National Family Health Survey — Fifth Round (NFHS-5) collected granular health and nutrition data across **707 districts** in all 28 states and 8 Union Territories between 2019 and 2021. Despite the richness of this dataset, translating raw survey figures into **actionable district-level health planning** remains a significant challenge for policymakers.

This platform addresses three core gaps:

- **Disparity Identification:** Surface districts with critical shortfalls in maternal health, child nutrition, sanitation, and healthcare access using objective, data-driven clustering.
- **Resource Prioritization:** Rank and group districts by intervention urgency so that limited public health budgets flow to the highest-need populations first.
- **Visual Accessibility:** Present complex multivariate health profiles through an interactive geospatial dashboard that district health officers and ministry planners can use without data science expertise.

The system processes **16 carefully selected public health indicators** using K-Means clustering to segment all 706 valid districts into three distinct health profiles, each demanding a different policy response.

---

## System Architecture

The platform is built as a two-tier system: an offline data science pipeline that produces cluster assignments and enriched district profiles, and an online serving layer consisting of a Streamlit visual dashboard and a FastAPI REST server.

```
   .-------------------------------------------------------.
   |               NFHS-5 Raw Dataset                      |
   |        706 Districts  x  500+ Survey Indicators       |
   '-------------------------------------------------------'
                             |
                             |
   .-------------------------------------------------------.
   |                    Data Audit                         |
   |     Missing value census, district name resolution,   |
   |     duplicate detection, column type inference        |
   '-------------------------------------------------------'
                             |
                             |
   .-------------------------------------------------------.
   |                   Data Cleaning                       |
   |    Imputation, standardisation, outlier treatment,    |
   |    district-state key normalisation                   |
   '-------------------------------------------------------'
                             |
                             |
   .-------------------------------------------------------.
   |         Feature Selection  --  16 Indicators          |
   |   Maternal Health  /  Child Nutrition  /  Sanitation  |
   |   Vaccination Coverage  /  Healthcare Access  /  OOP  |
   '-------------------------------------------------------'
                             |
                             |
   .-------------------------------------------------------.
   |           K-Means Clustering   K = 3                  |
   |   Elbow Method  +  Silhouette Analysis  +  PCA 2D     |
   '-------------------------------------------------------'
                             |
             .---------------+---------------.
            /                |                \
           /                 |                 \
   .------------.     .------------.     .------------.
   | Cluster 0  |     | Cluster 1  |     | Cluster 2  |
   | High       |     | High-Cost  |     | Healthcare |
   | Intervent. |     | Specific   |     | Leaders    |
   | 288 Dist.  |     | Risk       |     | 346 Dist.  |
   '------------'     | 72 Dist.   |     '------------'
                      '------------'
                             |
                             |
   .-------------------------------------------------------.
   |             Geographic Enrichment Layer               |
   |    GeoJSON district boundaries  +  Centroid join      |
   |    State-level aggregation  +  Choropleth prep        |
   '-------------------------------------------------------'
                             |
              .-------------' '-------------.
             /                               \
            /                                 \
   .-----------------.               .---------------------.
   |   Streamlit     |               |   FastAPI REST      |
   |   Dashboard     |               |   Server            |
   |   Port 8501     |               |   Port 8000         |
   |                 |               |                     |
   |  Choropleth Map |               |  /districts         |
   |  Cluster Filter |               |  /clusters          |
   |  District Cards |               |  /states            |
   |  Export Tools   |               |  /health-summary    |
   '-----------------'               '---------------------'
```

---

## Machine Learning Pipeline

### Stage 1 — Data Audit

`src/day1_audit.py` performs a full structural audit of the raw NFHS-5 Excel workbook:

- Counts missing values per column and flags indicators with more than 15% missingness
- Resolves district name inconsistencies against the official Census 2011 district list
- Generates an audit report saved to `outputs/audit_report.csv`

### Stage 2 — Data Cleaning

`src/day2_pipeline.py` applies a reproducible cleaning sequence:

- Median imputation for numeric indicators with low missingness
- District-level forward fill within states for geographically correlated indicators
- Min-Max normalisation scoped to the 16 selected features
- Saves cleaned frame to `outputs/cleaned_districts.csv`

### Stage 3 — Feature Selection

Sixteen indicators were selected from over 500 survey variables using domain knowledge combined with a low inter-correlation heuristic (Pearson r below 0.85 between any pair):

| Domain | Indicators Selected |
|---|---|
| Maternal Health | Institutional births, ANC 4+ visits, skilled birth attendance |
| Child Nutrition | Stunting rate, wasting rate, underweight prevalence |
| Vaccination | Full immunisation coverage, BCG, DPT3 |
| Sanitation | Open defecation free status, improved water source access |
| Healthcare Access | Distance to health facility, female literacy rate |
| Economic Burden | Out-of-pocket health expenditure share |

### Stage 4 — Clustering

`src/day3_clustering.py` runs the full unsupervised learning workflow:

- Elbow method tested K from 2 to 10; inertia curve inflects clearly at K=3
- Silhouette score at K=3 is 0.61, confirming well-separated clusters
- PCA reduces the 16-dimensional space to 2 components for visual validation
- Cluster assignments written back to the enriched district frame

---

## Cluster Topology and Profiles

The three clusters discovered by K-Means map cleanly onto three recognisable public health archetypes present in the Indian health literature.

```
                       706 DISTRICTS
                             |
             .---------------+---------------.
            /                                 \
           /                                   \
          /                                     \
   .-------------.                       .-------------.
   |  CLUSTER 0  |                       |  CLUSTER 2  |
   |             |                       |             |
   |    High     |                       |  Healthcare |
   | Intervention|                       |   Leaders   |
   |  Priority   |                       |             |
   |             |                       |             |
   | 288 Dist.   |                       | 346 Dist.   |
   '------+------'                       '------+------'
          |            .-----------.            |
          |           /             \           |
          |          |   CLUSTER 1   |          |
          |          |               |          |
          |          |  High-Cost    |          |
          |          |  Specific     |          |
          |          |  Risk         |          |
          |          |               |          |
          |          |   72 Dist.    |          |
          |           \             /           |
          |            '-----------'            |
          |                                     |
   .------+------.                       .------+------.
   |   Profile   |                       |   Profile   |
   |             |                       |             |
   | Stunting    |    .-------------.    | Strong ANC  |
   | Wasting     |    |   Profile   |    | Coverage    |
   | Open Defec. |    |             |    | Low         |
   | Low ANC     |    | Highest OOP |    | Stunting    |
   | Low Vacc.   |    | Tobacco Use |    | High Vacc.  |
   |             |    | Remote      |    | Low Open    |
   '------+------'    | Terrain     |    | Defecation  |
          |           '------+------'    '------+------'
          |                  |                  |
   .------+------.    .------+------.    .------+------.
   |  Key States |    |  Key States |    |  Key States |
   |             |    |             |    |             |
   | Uttar       |    | Arunachal   |    | Tamil Nadu  |
   | Pradesh     |    | Pradesh     |    | Kerala      |
   | Bihar       |    | Nagaland    |    | Karnataka   |
   | Madhya      |    | Meghalaya   |    | Andhra      |
   | Pradesh     |    | Manipur     |    | Pradesh     |
   | Jharkhand   |    | Mizoram     |    | Telangana   |
   '-------------'    '-------------'    '-------------'
```

### Cluster 0 — High Intervention Priority (288 districts)

Districts in this cluster represent the most acute public health burden in the country:

- **Child undernutrition:** Stunting prevalence above 38%, wasting above 18%, underweight above 34%
- **Sanitation deficit:** Open defecation rates remain among the highest nationally despite Swachh Bharat targets
- **Maternal care gap:** ANC 4+ visit compliance below 45%, institutional birth rates under 60% in many districts
- **Low vaccination:** Full immunisation coverage below 55%

**Policy implication:** These districts require immediate, intensive multi-programme convergence — POSHAN Abhiyaan nutrition missions, Mission Indradhanush vaccination drives, and accelerated Pradhan Mantri Matru Vandana Yojana coverage.

### Cluster 1 — High-Cost and Specific-Risk (72 districts)

A geographically concentrated cluster dominated by Northeastern states, characterised by a distinct risk profile:

- **Economic barrier:** Out-of-pocket health expenditure share is the highest nationally
- **Lifestyle risk:** Tobacco and alcohol use rates are significantly above the national median
- **Terrain and access:** Many districts are remote or hilly, with substantial distances to the nearest health facility
- **Nutrition profile:** Stunting and wasting are not as severe as Cluster 0, but micronutrient deficiencies are high

**Policy implication:** These districts need targeted financial protection schemes, substance use programmes, and infrastructure investment in last-mile health facility connectivity.

### Cluster 2 — Healthcare Leaders (346 districts)

The largest cluster by district count, concentrated in southern and western states:

- **Maternal health:** Institutional birth rates above 90%, ANC 4+ coverage above 75% in most districts
- **Child health:** Stunting prevalence below 18%, full immunisation above 80%
- **Sanitation:** Near-universal improved water source access, low open defecation
- **Healthcare access:** High female literacy correlates with high health-seeking behaviour

**Policy implication:** These districts serve as implementation models for transferring best practices to Cluster 0 districts.

---

## Directory Structure

```
   nfhs5-healthcare-analytics
   |
   .-- backend
   |       |
   |       .-- main.py                FastAPI application entry point
   |       .-- routers
   |       |       |
   |       |       .-- districts.py   District-level endpoints
   |       |       .-- clusters.py    Cluster summary endpoints
   |       |       '-- states.py      State aggregation endpoints
   |       .-- schemas.py             Pydantic request and response models
   |       '-- data_loader.py         Loads enriched CSV into memory at startup
   |
   .-- dashboard
   |       |
   |       .-- app.py                 Streamlit application entry point
   |       .-- pages
   |       |       |
   |       |       .-- overview.py    National summary and KPI cards
   |       |       .-- map_view.py    Interactive choropleth map
   |       |       .-- cluster_deep.py   Per-cluster drill-down view
   |       |       '-- district_cards.py District search and profile cards
   |       '-- components
   |               |
   |               .-- charts.py      Reusable Plotly chart builders
   |               '-- filters.py     Sidebar filter widgets
   |
   .-- geo
   |       |
   |       .-- india_districts.geojson    District boundary polygons
   |       .-- merge.py                   Joins cluster data to GeoJSON
   |       '-- outputs
   |               '-- enriched_map.geojson   Final map-ready GeoJSON
   |
   .-- src
   |       |
   |       .-- day1_audit.py          Data audit and quality census
   |       .-- day2_pipeline.py       Cleaning, imputation, normalisation
   |       .-- day3_clustering.py     K-Means training and assignment
   |       .-- day4_profiling.py      Cluster statistical profiling
   |       .-- day5_export.py         Final enriched CSV and report export
   |       '-- utils.py               Shared helpers
   |
   .-- data
   |       |
   |       .-- raw
   |       |       '-- nfhs5_district.xlsx    Original survey data
   |       '-- processed
   |               .-- cleaned_districts.csv  Post-pipeline cleaned frame
   |               '-- clustered_districts.csv   District frame with cluster labels
   |
   .-- outputs
   |       .-- audit_report.csv
   |       .-- elbow_curve.png
   |       .-- silhouette_plot.png
   |       .-- pca_scatter.png
   |       '-- cluster_profiles.csv
   |
   .-- notebooks
   |       .-- 01_eda.ipynb
   |       .-- 02_feature_selection.ipynb
   |       '-- 03_clustering_validation.ipynb
   |
   .-- requirements.txt
   .-- .env.example
   '-- README.md
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
| GeoPandas | 0.14+ | Geospatial joins and shapefile handling |

### Visualisation and Dashboard

| Library | Version | Role |
|---|---|---|
| Streamlit | 1.32+ | Interactive web dashboard |
| Plotly | 5.20+ | Choropleth maps and cluster charts |
| Matplotlib | 3.8+ | Offline diagnostic plots in notebooks |

### Backend API

| Library | Version | Role |
|---|---|---|
| FastAPI | 0.110+ | REST API framework |
| Uvicorn | 0.29+ | ASGI server |
| Pydantic | 2.6+ | Request and response schema validation |

---

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- `pip` 23+
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/nfhs5-healthcare-analytics.git
cd nfhs5-healthcare-analytics
```

### Step 2 — Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux or macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your local paths if needed
```

### Step 5 — Run the Data Science Pipeline

Execute the pipeline scripts in order. Each script reads from the previous stage's output.

```bash
# Stage 1: Audit the raw dataset
python src/day1_audit.py

# Stage 2: Clean and normalise
python src/day2_pipeline.py

# Stage 3: Run K-Means clustering
python src/day3_clustering.py

# Stage 4: Generate cluster profiles
python src/day4_profiling.py

# Stage 5: Export final enriched dataset
python src/day5_export.py

# Build map-ready GeoJSON
python geo/merge.py
```

After these steps, `data/processed/clustered_districts.csv` and `geo/outputs/enriched_map.geojson` will be ready to serve.

---

## Running the Application

### Streamlit Dashboard

The interactive dashboard runs on port **8501** by default.

```bash
streamlit run dashboard/app.py --server.port 8501
```

Open your browser at `http://localhost:8501`.

The dashboard provides:

- A national overview with cluster KPI cards and district counts
- A full-screen Plotly choropleth map of India coloured by cluster
- Per-cluster drill-down pages with box plots, scatter plots, and ranked tables
- A district search card that surfaces the full 16-indicator profile for any district
- CSV export of filtered district lists

### FastAPI REST Server

The API server runs on port **8000** by default.

```bash
uvicorn backend.main:app --reload --port 8000
```

Interactive API docs are auto-generated at `http://localhost:8000/docs`.

To run both services simultaneously in development, open two terminal windows and run one command in each.

---

## API Reference

All responses are JSON. The base URL in local development is `http://localhost:8000`.

### GET /districts

Returns the full list of 706 districts with cluster assignment and all 16 indicator values.

**Query parameters**

| Parameter | Type | Description |
|---|---|---|
| cluster | integer | Filter by cluster ID: 0, 1, or 2 |
| state | string | Filter by state name, URL-encoded |
| limit | integer | Maximum records to return, default 50 |
| offset | integer | Pagination offset, default 0 |

```bash
curl "http://localhost:8000/districts?cluster=0&state=Bihar&limit=10"
```

### GET /districts/{district_id}

Returns the full profile for a single district including its cluster, all 16 indicators, and state-level benchmark comparisons.

```bash
curl "http://localhost:8000/districts/UP_Gorakhpur"
```

### GET /clusters

Returns summary statistics — mean, median, min, max — for each of the 16 indicators broken down by cluster.

```bash
curl "http://localhost:8000/clusters"
```

### GET /clusters/{cluster_id}

Returns the detailed profile for a specific cluster including ranked indicator values and the list of constituent districts.

```bash
curl "http://localhost:8000/clusters/0"
```

### GET /states

Returns state-level aggregate statistics and the dominant cluster for each state.

```bash
curl "http://localhost:8000/states"
```

### GET /health-summary

Returns a high-level national summary: total districts processed, cluster distribution, and the five most critical indicators by national variance.

```bash
curl "http://localhost:8000/health-summary"
```

---

## Key Indicators

The 16 indicators used in clustering are listed below with their NFHS-5 survey variable codes for reproducibility.

| # | Indicator | NFHS-5 Code | Domain |
|---|---|---|---|
| 1 | Children stunted under 5 years % | CH_STNT_C_HA2 | Child Nutrition |
| 2 | Children wasted under 5 years % | CH_WAST_C_WH2 | Child Nutrition |
| 3 | Children underweight under 5 years % | CH_NUTR_C_WA2 | Child Nutrition |
| 4 | Full immunisation coverage 12-23 months % | CH_VACS_C_BAS | Vaccination |
| 5 | Institutional births % | RH_DELV_C_INS | Maternal Health |
| 6 | ANC 4 or more visits % | RH_ANC4_W_SKP | Maternal Health |
| 7 | Skilled birth attendance % | RH_DELA_C_SBA | Maternal Health |
| 8 | Households using improved drinking water % | WS_WATSN_H_IMP | Sanitation |
| 9 | Households practising open defecation % | WS_TLET_H_NON | Sanitation |
| 10 | Women with 10 or more years of schooling % | ED_LCMP_W_SEC | Female Education |
| 11 | Households with electricity % | HC_ELEC_H_ELC | Infrastructure |
| 12 | Out-of-pocket health expenditure share % | HC_HEXP_H_OOP | Economic Burden |
| 13 | Women who use tobacco % | TO_TOBA_W_ANY | Lifestyle Risk |
| 14 | Men who use tobacco % | TO_TOBA_M_ANY | Lifestyle Risk |
| 15 | Women aged 15-49 who are anaemic % | AN_ANEM_W_ANY | Maternal Health |
| 16 | Children aged 6-59 months who are anaemic % | AN_ANEM_C_ANY | Child Nutrition |

---

## Reproducibility

The entire pipeline from raw data to cluster assignments is deterministic given a fixed random seed. The random state is set globally at the top of `day3_clustering.py`:

```python
RANDOM_STATE = 42
```

All intermediate outputs are versioned in `outputs/` with timestamps when running in production mode. To reproduce results from scratch, delete `data/processed/` and rerun the pipeline scripts in order.

---

## Acknowledgements

- **Ministry of Health and Family Welfare, Government of India** — for making NFHS-5 district-level data publicly available
- **International Institute for Population Sciences, Mumbai** — for conducting and publishing the NFHS-5 survey
- **Survey of India** — for the district boundary shapefiles used in geospatial visualisation
- **Scikit-Learn contributors** — for the robust implementation of K-Means and PCA used in this pipeline

---

## License

This project is released under the MIT License. The underlying NFHS-5 data is published by the Government of India and is in the public domain for research and non-commercial use.

---

*Built with Python, Scikit-Learn, Streamlit, and FastAPI. Data sourced from NFHS-5 2019-21.*
