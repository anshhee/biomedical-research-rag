import json
from pathlib import Path

import requests


def extract_trial(study):
    protocol = study["protocolSection"]

    identification = protocol["identificationModule"]
    status = protocol["statusModule"]
    conditions = protocol["conditionsModule"]
    design = protocol["designModule"]

    trial = {
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "official_title": identification.get("officialTitle"),
        "status": status.get("overallStatus"),
        "conditions": conditions.get("conditions", []),
        "keywords": conditions.get("keywords", []),
        "study_type": design.get("studyType"),
        "phase": design.get("phases", []),
        "enrollment": design.get("enrollmentInfo", {}).get("count"),
    }

    return trial

#fetching trails from the Clinical Trials API

def fetch_trials(query_condition, query_term, max_trials=1000):
    url = "https://clinicaltrials.gov/api/v2/studies"

    params = {
        "query.cond": query_condition,
        "query.term": query_term,
        "pageSize": 100,
    }

    all_trials = []

    while len(all_trials) < max_trials:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for study in data.get("studies", []):
            trial = extract_trial(study)
            all_trials.append(trial)

            if len(all_trials) >= max_trials:
                break

        next_token = data.get("nextPageToken")

        if not next_token:
            break

        params["pageToken"] = next_token

    return all_trials


# Fetch trials
trials = fetch_trials(
    query_condition="prostate cancer",
    query_term="radioligand",
    max_trials=1000,
)


# Data quality check
print("\n--- DATA QUALITY CHECK ---")

fields = [
    "nct_id",
    "title",
    "official_title",
    "status",
    "conditions",
    "keywords",
    "study_type",
    "phase",
    "enrollment",
]

for field in fields:
    missing = sum(
        1
        for trial in trials
        if not trial.get(field)
    )

    print(f"{field}: {missing} missing")


# Duplicate check
print("\n--- DUPLICATE CHECK ---")

nct_ids = [trial["nct_id"] for trial in trials]
unique_ids = set(nct_ids)

print("Total trials:", len(nct_ids))
print("Unique NCT IDs:", len(unique_ids))
print("Duplicate trials:", len(nct_ids) - len(unique_ids))


# Save trial data
output_dir = Path("data/processed")
output_dir.mkdir(exist_ok=True, parents=True)

output_file = output_dir / "clinical_trials.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        trials,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("\nTotal trials collected:", len(trials))
print("Saved to:", output_file)