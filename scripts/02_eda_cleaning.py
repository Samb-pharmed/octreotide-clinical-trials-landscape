# scripts/02_eda_cleaning.py

import pandas as pd
from pathlib import Path


# =========================
# 1. Define project paths
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "clinical_trials_octreotide.xlsx"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = PROCESSED_DIR / "clinical_trials_octreotide_cleaned.xlsx"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Load raw data
# =========================

print("Loading raw clinical trials data...")

df = pd.read_excel(RAW_DATA_PATH)

print(f"Data loaded successfully.")
print(f"Shape of raw dataset: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())


# =========================
# 3. Basic dataset inspection
# =========================

print("\n==============================")
print("BASIC DATASET INFORMATION")
print("==============================")

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset info:")
print(df.info())

print("\nMissing values per column:")
missing_values = df.isna().sum().sort_values(ascending=False)
print(missing_values)

print("\nDuplicate rows:")
print(df.duplicated().sum())


# =========================
# 4. Standardise column names
# =========================

print("\nCleaning column names...")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("/", "_")
)

print("Cleaned column names:")
print(df.columns.tolist())


# =========================
# 5. Remove exact duplicate rows
# =========================

before_rows = len(df)
df = df.drop_duplicates()
after_rows = len(df)

print(f"\nRemoved {before_rows - after_rows} duplicate rows.")


# =========================
# 6. Clean text columns
# =========================

print("\nCleaning text columns...")

text_columns = df.select_dtypes(include="object").columns

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

print("\nStandardising sponsor names...")

if "sponsor" in df.columns:
    sponsor_name_mapping = {
        "Novartis Pharmaceuticals": "Novartis",
        "Novartis Pharmaceuticals Corporation": "Novartis",
        "Novartis Pharma Services AG": "Novartis",
        "Novartis": "Novartis"
    }

    df["sponsor"] = df["sponsor"].replace(sponsor_name_mapping)

    print("Sponsor names standardised.")
else:
    print("sponsor column not found.")

# =========================
# 7. Convert date columns
# =========================

print("\nConverting date columns...")

possible_date_columns = [
    "start_date",
    "completion_date",
    "primary_completion_date",
    "study_first_submit_date",
    "last_update_submit_date",
    "results_first_submit_date"
]

for col in possible_date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        print(f"Converted to datetime: {col}")


# =========================
# 8. Create trial duration column
# =========================

print("\nCreating trial duration column...")

if "start_date" in df.columns and "completion_date" in df.columns:
    df["trial_duration_days"] = (df["completion_date"] - df["start_date"]).dt.days
    df["trial_duration_months"] = (df["trial_duration_days"] / 30.44).round(1)

    print("Created: trial_duration_days")
    print("Created: trial_duration_months")
else:
    print("Start date or completion date not found. Trial duration was not created.")


# =========================
# 9. Clean enrolment column
# =========================

print("\nCleaning enrollment column...")

if "enrollment_count" in df.columns:
    df["enrollment_count"] = pd.to_numeric(df["enrollment_count"], errors="coerce")
    print("Converted enrollment_count to numeric.")
elif "enrollment" in df.columns:
    df["enrollment"] = pd.to_numeric(df["enrollment"], errors="coerce")
    print("Converted enrollment to numeric.")
else:
    print("No enrollment column found.")


# =========================
# 10. Create study year column
# =========================

print("\nCreating study year column...")

if "start_date" in df.columns:
    df["start_year"] = df["start_date"].dt.year
    print("Created: start_year")


# =========================
# 11. Identify interventional vs observational studies
# =========================

print("\nChecking study type distribution...")

if "study_type" in df.columns:
    print(df["study_type"].value_counts(dropna=False))
else:
    print("study_type column not found.")


# =========================
# 12. Key categorical summaries
# =========================

print("\n==============================")
print("KEY CATEGORICAL SUMMARIES")
print("==============================")

categorical_columns_to_check = [
    "overall_status",
    "phase",
    "study_type",
    "intervention_type",
    "lead_sponsor_name",
    "sex",
    "healthy_volunteers"
]

for col in categorical_columns_to_check:
    if col in df.columns:
        print(f"\nTop values in {col}:")
        print(df[col].value_counts(dropna=False).head(10))


# =========================
# 13. Numeric summaries
# =========================

print("\n==============================")
print("NUMERIC SUMMARIES")
print("==============================")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

if len(numeric_cols) > 0:
    print(df[numeric_cols].describe())
else:
    print("No numeric columns found.")


# =========================
# 14. Save cleaned dataset
# =========================

print("\nSaving cleaned dataset...")

df.to_excel(OUTPUT_PATH, index=False)

print(f"Cleaned dataset saved to:")
print(OUTPUT_PATH)

print("\nStage 2 EDA and cleaning completed successfully.")