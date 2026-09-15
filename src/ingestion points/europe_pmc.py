import requests
import json
from pathlib import Path


# extracting research paper from europe_pmc using api

def extract_paper(result):
    paper =  {
        "id": result.get("id"),
        "source": result.get("source"),
        "doi": result.get("doi"),
        "title": result.get("title"),
        "authors": result.get("authorString"),
        "publication_year": result.get("pubYear"),
        "publication_type": result.get("pubTypeList", {}).get("pubType", []),
        "is_open_access": result.get("isOpenAccess"),
        "citation_count": result.get("citedByCount"),
        "abstract": result.get("abstractText"),
        "full_text_urls": result.get("fullTextUrlList", {}).get("fullTextUrl", []),
    }

    return paper 

url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

params = {
    "query": "prostate cancer radioligand",
    "format": "json",
    "resultType": "core",
}

# fetching papers 

def fetch_papers(query, max_papers=1000):
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": 100,
        "cursorMark": "*",
    }

    all_papers = []

    while len(all_papers) < max_papers:

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        results = data.get("resultList", {}).get("result", [])

        for result in results:
            paper = extract_paper(result)
            all_papers.append(paper)

            if len(all_papers) >= max_papers:
                break

        next_cursor = data.get("nextCursorMark")

        if not next_cursor:
            break

        params["cursorMark"] = next_cursor

    return all_papers


papers = fetch_papers(
    query="prostate cancer radioligand",
    max_papers=1000
)

print("Total papers collected:", len(papers))

print("\nFirst paper:")
print(papers[0])
print("\n--- DATA QUALITY CHECK ---")

fields = [
    "id",
    "title",
    "authors",
    "publication_year",
    "abstract",
    "doi",
    "publication_type"
]

for field in fields:
    missing = sum(
        1 for paper in papers
        if not paper.get(field)
    )

    print(f"{field}: {missing} missing")


    print("\n--- DUPLICATE CHECK ---")

paper_ids = [paper["id"] for paper in papers]

unique_ids = set(paper_ids)

print("Total papers:", len(paper_ids))
print("Unique IDs:", len(unique_ids))
print("Duplicate papers:", len(paper_ids) - len(unique_ids))



print("\n--- ABSTRACT CHECK ---")

papers_with_abstract = sum(
    1 for paper in papers
    if paper.get("abstract")
)

print("Papers with abstracts:", papers_with_abstract)
print("Papers without abstracts:", len(papers) - papers_with_abstract)


# Save paper data

output_dir = Path("data/processed")
output_dir.mkdir(exist_ok=True, parents=True)

output_file = output_dir / "europe_pmc_papers.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

print("\nSaved to:", output_file)