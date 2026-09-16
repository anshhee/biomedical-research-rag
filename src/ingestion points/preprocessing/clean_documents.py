import json
from html import unescape 
import re  
from pathlib import Path

# Paths to our ingested data

clinical_trials_file = Path("data/processed/clinical_trials.json")
europe_pmc_file = Path("data/processed/europe_pmc_papers.json")

with open(clinical_trials_file, "r", encoding="utf-8") as f:
    clinical_trials = json.load(f)




#loading Europe PMC papers data
with open(europe_pmc_file, "r", encoding="utf-8") as f:
    europe_pmc_papers  = json.load(f)



#convert clinical trial into document

def trial_to_document(trial):
    document = {
        "doc_id": trial["nct_id"],
        "source": "clinical_trials",
        "title": trial["title"],
        "text": (
            f"Title: {trial['title']}\n"
            f"Official Title: {trial.get('official_title', '')}\n"
            f"Conditions: {', '.join(trial.get('conditions', []))}\n"
            f"Keywords: {', '.join(trial.get('keywords', []))}"
        ),
        "metadata": {
            "nct_id": trial["nct_id"],
            "status": trial.get("status"),
            "study_type": trial.get("study_type"),
            "phase": trial.get("phase", []),
            "enrollment": trial.get("enrollment"),
        }
    }

    return document


# paper to document 

def paper_to_document(paper):
    document = {
        "doc_id": paper["id"],
        "source": "europe_pmc",
        "title": paper["title"],
        "text": (
            f"Title: {paper.get('title', '')}\n"
            f"Abstract: {paper.get('abstract', '')}"
        ),
        "metadata": {
            "doi": paper.get("doi"),
            "authors": paper.get("authors"),
            "publication_year": paper.get("publication_year"),
            "publication_type": paper.get("publication_type", []),
            "is_open_access": paper.get("is_open_access"),
            "citation_count": paper.get("citation_count"),
        }
    }

    return document

# complete trial docs
trial_documents = []

for trial in clinical_trials:
    document = trial_to_document(trial)
    trial_documents.append(document)


# complete paper documents 
paper_documents = []

for paper in europe_pmc_papers:
    document = paper_to_document(paper)
    paper_documents.append(document)
    

# combined and cleaned docs

documents = trial_documents + paper_documents


#doc cleaner func

def clean_text(text):
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
    


# cleaning all the 1000+ docs 

cleaned_documents = []

for document in documents:
    cleaned_document = document.copy()
    cleaned_document["text"] = clean_text(document["text"])
    cleaned_documents.append(cleaned_document)

print("\n--- CLEANED DOCUMENTS ---")
print("Total cleaned documents:", len(cleaned_documents))
print("First cleaned document:")
print(cleaned_documents[0])


output_file = Path("data/processed/cleaned_documents.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_documents, f, indent=2, ensure_ascii=False)

print("Saved to:", output_file)