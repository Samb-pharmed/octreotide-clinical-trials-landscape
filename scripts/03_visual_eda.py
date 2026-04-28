# scripts/03_visual_eda.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Define project paths
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed" / "clinical_trials_octreotide_cleaned.xlsx"

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Load cleaned data
# =========================

print("Loading cleaned clinical trials dataset...")

df = pd.read_excel(INPUT_PATH)

print(f"Dataset loaded successfully.")
print(f"Shape: {df.shape}")
print(df.head())


# =========================
# 3. Helper function for Excel dates
# =========================

def convert_excel_or_normal_date(series):
    """
    Converts a date column safely.
    It handles:
    1. normal date strings
    2. pandas datetime values
    3. Excel serial date numbers
    """

    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, origin="1899-12-30", unit="D", errors="coerce")
    else:
        return pd.to_datetime(series, errors="coerce")


# =========================
# 4. Ensure correct data types
# =========================

print("\nChecking and fixing data types...")

date_columns = ["start_date", "completion_date"]

for col in date_columns:
    if col in df.columns:
        df[col] = convert_excel_or_normal_date(df[col])
        print(f"Converted date column: {col}")

if "start_year" not in df.columns and "start_date" in df.columns:
    df["start_year"] = df["start_date"].dt.year

if "trial_duration_days" not in df.columns and {"start_date", "completion_date"}.issubset(df.columns):
    df["trial_duration_days"] = (df["completion_date"] - df["start_date"]).dt.days
    df["trial_duration_months"] = (df["trial_duration_days"] / 30.44).round(1)

if "enrollment" in df.columns:
    df["enrollment"] = pd.to_numeric(df["enrollment"], errors="coerce")

if "trial_duration_days" in df.columns:
    df["trial_duration_days"] = pd.to_numeric(df["trial_duration_days"], errors="coerce")

if "trial_duration_months" in df.columns:
    df["trial_duration_months"] = pd.to_numeric(df["trial_duration_months"], errors="coerce")


# =========================
# 5. Simple plotting function
# =========================

def save_bar_chart(data, title, xlabel, ylabel, filename, rotation=45):
    plt.figure(figsize=(10, 6))
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()

    output_path = FIGURES_DIR / filename
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure: {output_path}")


# =========================
# 6. Trial status distribution
# =========================

print("\nCreating status distribution chart...")

if "status" in df.columns:
    status_counts = df["status"].value_counts(dropna=False)

    save_bar_chart(
        data=status_counts,
        title="Octreotide Clinical Trials by Recruitment Status",
        xlabel="Trial Status",
        ylabel="Number of Trials",
        filename="01_trial_status_distribution.png"
    )

    status_counts.to_excel(TABLES_DIR / "status_counts.xlsx")


# =========================
# 7. Trial phase distribution
# =========================

print("\nCreating phase distribution chart...")

if "phase" in df.columns:
    phase_counts = df["phase"].fillna("MISSING").value_counts()

    save_bar_chart(
        data=phase_counts,
        title="Octreotide Clinical Trials by Phase",
        xlabel="Clinical Trial Phase",
        ylabel="Number of Trials",
        filename="02_phase_distribution.png"
    )

    phase_counts.to_excel(TABLES_DIR / "phase_counts.xlsx")


# =========================
# 8. Trials by start year
# =========================

print("\nCreating trials by start year chart...")

if "start_year" in df.columns:
    year_counts = df["start_year"].dropna().astype(int).value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    year_counts.plot(kind="line", marker="o")
    plt.title("Octreotide Clinical Trials Started per Year")
    plt.xlabel("Start Year")
    plt.ylabel("Number of Trials")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURES_DIR / "03_trials_by_start_year.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure: {output_path}")

    year_counts.to_excel(TABLES_DIR / "trials_by_start_year.xlsx")


# =========================
# 9. Top sponsors
# =========================

print("\nCreating top sponsors chart...")

if "sponsor" in df.columns:
    top_sponsors = df["sponsor"].value_counts().head(15)

    save_bar_chart(
        data=top_sponsors,
        title="Top Sponsors in Octreotide Clinical Trials",
        xlabel="Sponsor",
        ylabel="Number of Trials",
        filename="04_top_sponsors.png"
    )

    top_sponsors.to_excel(TABLES_DIR / "top_sponsors.xlsx")


# =========================
# 10. Enrollment distribution
# =========================

print("\nCreating enrollment distribution chart...")

if "enrollment" in df.columns:
    enrollment_data = df["enrollment"].dropna()

    plt.figure(figsize=(10, 6))
    plt.hist(enrollment_data, bins=20)
    plt.title("Enrollment Distribution in Octreotide Clinical Trials")
    plt.xlabel("Enrollment Count")
    plt.ylabel("Number of Trials")
    plt.tight_layout()

    output_path = FIGURES_DIR / "05_enrollment_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure: {output_path}")


# =========================
# 11. Trial duration distribution
# =========================

print("\nCreating trial duration distribution chart...")

if "trial_duration_months" in df.columns:
    duration_data = df["trial_duration_months"].dropna()

    plt.figure(figsize=(10, 6))
    plt.hist(duration_data, bins=20)
    plt.title("Trial Duration Distribution for Octreotide Clinical Trials")
    plt.xlabel("Trial Duration, months")
    plt.ylabel("Number of Trials")
    plt.tight_layout()

    output_path = FIGURES_DIR / "06_trial_duration_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure: {output_path}")


# =========================
# 12. Status by phase table
# =========================

print("\nCreating status by phase summary table...")

if {"status", "phase"}.issubset(df.columns):
    status_by_phase = pd.crosstab(
        df["phase"].fillna("MISSING"),
        df["status"].fillna("MISSING")
    )

    status_by_phase.to_excel(TABLES_DIR / "status_by_phase.xlsx")

    print("Saved table: status_by_phase.xlsx")


# =========================
# 13. Portfolio summary table
# =========================

print("\nCreating portfolio summary table...")

summary = {
    "metric": [
        "Total trials",
        "Completed trials",
        "Recruiting trials",
        "Terminated trials",
        "Trials with missing phase",
        "Median enrollment",
        "Maximum enrollment",
        "Median trial duration months",
        "Maximum trial duration months"
    ],
    "value": [
        len(df),
        (df["status"] == "COMPLETED").sum() if "status" in df.columns else None,
        (df["status"] == "RECRUITING").sum() if "status" in df.columns else None,
        (df["status"] == "TERMINATED").sum() if "status" in df.columns else None,
        df["phase"].isna().sum() if "phase" in df.columns else None,
        df["enrollment"].median() if "enrollment" in df.columns else None,
        df["enrollment"].max() if "enrollment" in df.columns else None,
        df["trial_duration_months"].median() if "trial_duration_months" in df.columns else None,
        df["trial_duration_months"].max() if "trial_duration_months" in df.columns else None,
    ]
}

summary_df = pd.DataFrame(summary)

summary_output_path = TABLES_DIR / "portfolio_summary.xlsx"
summary_df.to_excel(summary_output_path, index=False)

print(f"Saved summary table: {summary_output_path}")


# =========================
# 14. Finish
# =========================

print("\nStage 3 visual EDA completed successfully.")
print(f"Figures saved in: {FIGURES_DIR}")
print(f"Tables saved in: {TABLES_DIR}")