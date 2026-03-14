import json
import time

import requests

CASES = {
    "caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "cumene": "CC(C)c1ccccc1",
    "choline_like_testcase": "CCCCCCCCC[NH+]1C[C@@H]([C@H]([C@@H]([C@H]1CO)O)O)O",
}


def structure_search(smiles: str) -> dict:
    payload = {
        "StructureSearchRequest": {
            "struct": smiles,
            "structSearchType": "exact",
            "maxResults": 10,
        }
    }
    response = requests.post(
        "https://www.surechembl.org/api/search/structure",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def fetch_results(search_hash: str) -> dict:
    for _ in range(5):
        time.sleep(2)
        response = requests.get(
            f"https://www.surechembl.org/api/search/{search_hash}/results",
            params={"page": 1, "max_results": 10},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json().get("data", {})
        if payload.get("results") is not None:
            return response.json()
    raise RuntimeError("search results not ready")


def fetch_documents(chemical_id: str) -> dict:
    response = requests.post(
        "https://www.surechembl.org/api/search/documents_for_structures",
        params={"chemicalIds": chemical_id, "page": 1, "itemsPerPage": 5},
        timeout=60,
    )
    return {
        "status_code": response.status_code,
        "body": response.json() if response.content else None,
    }


def main():
    report = {}
    for label, smiles in CASES.items():
        search = structure_search(smiles)
        search_hash = search["data"]["hash"]
        results = fetch_results(search_hash)
        structures = results["data"]["results"]["structures"]
        exact_structures = [item for item in structures if item.get("smiles") == smiles]
        report[label] = {
            "input_smiles": smiles,
            "search_hash": search_hash,
            "total_hits": results["data"]["results"]["total_hits"],
            "returned_structures": structures,
            "exact_structure_ids": [item["id"] for item in exact_structures],
            "documents_for_exact_ids": {
                item["id"]: fetch_documents(item["id"]) for item in exact_structures
            },
        }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
