import json
import os
from time import sleep

from dotenv import load_dotenv

from chemcrow.tools.rxn4chem import RXNPredict


def main():
    load_dotenv()
    sleep(2)
    tool = RXNPredict(
        os.environ["RXN4CHEM_API_KEY"],
        project_id=os.environ["RXN4CHEM_PROJECT_ID"],
    )
    reactants = "CCO.O=O"
    result = tool._run(reactants)
    print(
        json.dumps(
            {
                "reactants": reactants,
                "product": result,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
