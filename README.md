# Octreotide Clinical Trials Landscape Analysis

## Overview

This project analyses octreotide-related clinical trials using data extracted from the ClinicalTrials.gov API v2.

The goal is to demonstrate a pharma-focused data science workflow covering data extraction, data cleaning, exploratory data analysis, visualisation, and clinical trial landscape interpretation.

## Data Source

Data source: ClinicalTrials.gov API v2  
Search term: `octreotide`

Raw dataset:

```text
data/raw/clinical_trials_octreotide.xlsx
```

Cleaned dataset:

```text
data/processed/clinical_trials_octreotide_cleaned.xlsx
```

## Workflow

```text
01_download_clinical_trials.py
        ↓
02_eda_cleaning.py
        ↓
03_visual_eda.py
        ↓
04_trial_landscape_summary.py
        ↓
01_octreotide_clinical_trials_eda.ipynb
```

## Repository Structure

```text
clinical_trials_project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
│   ├── figures/
│   └── tables/
├── scripts/
├── README.md
└── requirements.txt
```

## Key Outputs

The project generates:

- cleaned clinical trial dataset
- trial status distribution chart
- phase distribution chart
- trial activity by start year
- top sponsor analysis
- enrollment distribution
- trial duration distribution
- Excel summary report
- Word interpretation report
- portfolio-ready Jupyter notebook

## Key Findings

The cleaned dataset contains 100 octreotide-related clinical trial records.

Initial analysis showed that:

- many trials were completed, indicating a mature clinical development landscape
- Phase 2 and Phase 3 studies represented a major part of the dataset
- sponsor names required standardisation due to inconsistent naming in ClinicalTrials.gov
- enrollment size varied widely across trials
- trial duration varied substantially, likely reflecting differences in indication, endpoint type, study design, and follow-up duration

## Skills Demonstrated

- Python scripting
- API data extraction
- pandas-based data cleaning
- exploratory data analysis
- matplotlib visualisation
- Excel and Word report generation
- pharma-focused clinical trial interpretation
- portfolio project organisation


## Disclaimer

This project uses publicly available clinical trial registry data for educational and portfolio purposes. The analysis is exploratory and should not be interpreted as regulatory, clinical, or investment advice.
