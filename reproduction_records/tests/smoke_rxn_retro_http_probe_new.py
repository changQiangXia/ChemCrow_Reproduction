import json
import os

import requests
from dotenv import load_dotenv
from rxn4chemistry import RXN4ChemistryWrapper


def main():
    load_dotenv()
    client = RXN4ChemistryWrapper(
        api_key=os.environ["RXN4CHEM_API_KEY"],
        base_url="https://rxn.res.ibm.com",
    )
    client.project_id = os.environ["RXN4CHEM_PROJECT_ID"]
    payload = {
        "product": "CC(=O)Oc1ccccc1C(=O)O",
        "fap": 0.6,
        "max_steps": 3,
        "nbeams": 10,
        "pruning_steps": 2,
        "ai_model": "12class-tokens-2021-05-14",
    }
    response = requests.post(
        client.routes.retrosynthesis_prediction_url,
        headers=client.headers,
        data=json.dumps(payload),
        cookies={},
        params={"projectId": client.project_id},
        timeout=60,
    )
    print(
        json.dumps(
            {
                "status_code": response.status_code,
                "body": response.json(),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
