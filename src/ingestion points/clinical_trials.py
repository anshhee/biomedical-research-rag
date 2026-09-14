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


url = "https://clinicaltrials.gov/api/v2/studies"

params = {
    "query.cond": "prostate cancer",
    "query.term": "radioligand"
}

#fetch trials 

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


trials = fetch_trials(
    query_condition="prostate cancer",
     query_term="radioligand",
     max_trials=1000
)

print("Total trials collected:", len(trials))
print("\nFirst trial:")
print(trials[0])