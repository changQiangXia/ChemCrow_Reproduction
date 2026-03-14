import json
import os

from dotenv import load_dotenv
from rxn4chemistry import RXN4ChemistryWrapper


def main():
    load_dotenv()
    client = RXN4ChemistryWrapper(
        api_key=os.environ["RXN4CHEM_API_KEY"],
        base_url="https://rxn.res.ibm.com",
    )
    client.project_id = os.environ["RXN4CHEM_PROJECT_ID"]
    projects = client.list_all_projects(size=5)
    payload = projects.get("response", {}).get("payload", {})
    content = payload.get("content", [])
    print(
        json.dumps(
            {
                "project_id": client.project_id,
                "project_count": payload.get("totalElements"),
                "project_ids": [item.get("id") for item in content if item.get("id")],
                "project_found": any(
                    item.get("id") == client.project_id for item in content
                ),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
