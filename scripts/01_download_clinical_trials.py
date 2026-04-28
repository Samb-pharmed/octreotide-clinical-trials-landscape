import requests
import pandas as pd
from pathlib import Path


BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_clinical_trials(search_term: str, page_size: int = 100):
    params = {
        "query.term": search_term,
        "pageSize": page_size,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def parse_studies(data):
    rows = []

    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})

        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions = protocol.get("conditionsModule", {})
        sponsor = protocol.get("sponsorCollaboratorsModule", {})

        rows.append({
            "nct_id": identification.get("nctId"),
            "title": identification.get("briefTitle"),
            "status": status.get("overallStatus"),
            "start_date": status.get("startDateStruct", {}).get("date"),
            "completion_date": status.get("completionDateStruct", {}).get("date"),
            "phase": ", ".join(design.get("phases", [])) if design.get("phases") else None,
            "conditions": ", ".join(conditions.get("conditions", [])) if conditions.get("conditions") else None,
            "sponsor": sponsor.get("leadSponsor", {}).get("name"),
            "enrollment": design.get("enrollmentInfo", {}).get("count"),
        })

    return pd.DataFrame(rows)


def main():
    search_term = "octreotide"

    print(f"Downloading clinical trials for: {search_term}")

    data = fetch_clinical_trials(search_term)
    df = parse_studies(data)

    output_path = RAW_DATA_DIR / "clinical_trials_octreotide.xlsx"
    df.to_excel(output_path, index=False)

    print(f"Saved {len(df)} studies to:")
    print(output_path)


if __name__ == "__main__":
    main()