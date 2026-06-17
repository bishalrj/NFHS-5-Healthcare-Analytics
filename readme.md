# NFHS-5 Healthcare Analytics and District-Level Planning System

## Overview

The NFHS-5 Healthcare Analytics and District-Level Planning System is a data-driven public health analytics platform built using district-level data from India's National Family Health Survey (NFHS-5).

The project applies unsupervised machine learning to identify healthcare development patterns across 706 Indian districts and provides interactive analytics through geographic visualizations, dashboards, and REST APIs.

---

## Problem Statement

India exhibits significant disparities in healthcare access, maternal and child health outcomes, sanitation, nutrition, and healthcare infrastructure across districts.

To enable targeted policy interventions and evidence-based resource allocation, healthcare planners require an analytical framework capable of identifying district-level healthcare typologies and exposing regional disparities through accessible visual interfaces.

This project addresses that challenge using district-level NFHS-5 indicators and unsupervised learning.

---

## Dataset

**Source:** National Family Health Survey (NFHS-5)

### Coverage

* 706 Districts
* 109 Original Indicators

### Final Modeling Dataset

* 16 Selected Healthcare Indicators
* 706 Districts
* Cleaned and Imputed Data
* Standardized Features
* Zero Missing Values

### Domains Covered

* Demographics
* Education
* Maternal Health
* Child Health
* Nutrition
* Sanitation
* Lifestyle Risk Factors
* Healthcare Access

---

## Methodology

### 1. Data Audit

* Dataset exploration
* Missing value assessment
* Data type validation
* Feature inventory generation

### 2. Data Cleaning

* Removal of NFHS formatting artifacts
* Numeric conversion
* Median imputation
* Outlier handling through Winsorization

### 3. Feature Selection

Selected 16 representative indicators spanning:

* Social determinants
* Maternal health
* Child health
* Nutrition
* Sanitation
* Healthcare accessibility

### 4. Clustering

Algorithm:

* K-Means Clustering

Preprocessing:

* StandardScaler

Model Selection:

* Elbow Method
* Silhouette Score

Optimal Clusters:

* K = 3

### 5. Geographic Analysis

* State-level cluster aggregation
* Geographic intelligence layer
* Interactive choropleth mapping
* Regional healthcare disparity analysis

---

## Project Architecture

```text
NFHS-5 Dataset
        │
        ▼
Data Audit
        │
        ▼
Data Cleaning
        │
        ▼
Feature Selection
        │
        ▼
Model Ready Dataset
        │
        ▼
K-Means Clustering
        │
        ▼
Cluster Interpretation
        │
        ▼
State-Level Analysis
        │
        ▼
Geographic Intelligence Layer
        │
        ▼
Streamlit Dashboard
        │
        ▼
FastAPI Service Layer
```

---

## Cluster Profiles

### Cluster 0 — High Intervention Priority Districts

**Districts:** 288

Characteristics:

* Highest child stunting rates
* High female undernutrition
* Poor sanitation access
* Low maternal healthcare utilization
* Low clean cooking fuel adoption

---

### Cluster 1 — High-Cost & Specific-Risk Districts

**Districts:** 72

Characteristics:

* Highest out-of-pocket healthcare expenditure
* High tobacco usage
* Lower institutional birth rates
* Better female education indicators

---

### Cluster 2 — Healthcare Leaders

**Districts:** 346

Characteristics:

* Highest vaccination coverage
* Strong maternal healthcare performance
* Better sanitation infrastructure
* Better healthcare accessibility
* Lowest child stunting prevalence

---

## Key Findings

### High Intervention Priority States

* Uttar Pradesh
* Bihar
* Madhya Pradesh
* Jharkhand
* Assam

### High-Cost & Specific-Risk States

* Arunachal Pradesh
* Nagaland
* Meghalaya
* Manipur
* Mizoram

### Healthcare Leader States

* Tamil Nadu
* Kerala
* Telangana
* Karnataka
* Punjab

---

## Dashboard Features

### Overview

* Project summary
* Cluster distribution
* High-level healthcare insights

### District Explorer

* District-level healthcare indicators
* Cluster assignment
* Comparative analysis

### Cluster Explorer

* Cluster profiles
* Cluster statistics
* Indicator comparisons

### State Analysis

* State-level cluster distributions
* Regional performance insights

### Geographic Analysis

* Interactive healthcare maps
* Cluster concentration visualization
* Geographic disparity exploration

---

## FastAPI Endpoints

### System

* `GET /`

### Districts

* `GET /districts`
* `GET /district/{district_name}`

### States

* `GET /states`
* `GET /state/{state_name}`

### Clusters

* `GET /clusters`
* `GET /cluster/{cluster_id}`

---

## Technology Stack

### Data Science & Machine Learning

* Python
* Pandas
* NumPy
* Scikit-Learn

### Dashboard

* Streamlit
* Plotly

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Geospatial Analytics

* GeoPandas
* Folium

---

## Folder Structure

```text
nfhs-healthcare-analytics/
│
├── backend/
├── dashboard/
├── geo/
├── reports/
├── src/
│
├── day2_pipeline.py
├── day3_clustering.py
├── day4_analysis.py
├── day5_state_analysis.py
├── generate_maps.py
│
├── README.md
└── requirements.txt
```

---

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## Running the Backend

```bash
python -m backend.main
```

or

```bash
uvicorn backend.main:app --reload
```

API URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Project Results

* Processed 706 Indian districts across 16 healthcare indicators.
* Identified 3 healthcare development typologies using unsupervised learning.
* Reconstructed regional healthcare disparities without geographic inputs.
* Developed state-level geographic intelligence visualizations.
* Built a multi-page Streamlit analytics dashboard.
* Exposed healthcare insights through FastAPI APIs.

---

## Limitations

* Administrative boundary differences between NFHS-5 districts and available GeoJSON datasets resulted in a 70.7% exact district match rate.
* State-level aggregation was used for geospatial visualization due to district boundary mismatches.
* Newly created districts are not represented in the legacy geographic boundary dataset.

---

## Future Improvements

* Updated district boundary integration
* District-level choropleth mapping
* Healthcare trend monitoring across NFHS rounds
* Advanced policy simulation tools
* Automated healthcare reporting workflows

---

## Author

**Bishal Raj Kakoti**

B.Tech Computer Science & Engineering (Data Science)

Jain (Deemed-to-be University)

---

*Built using machine learning, geospatial analytics, and public health data to support evidence-based healthcare planning.*
