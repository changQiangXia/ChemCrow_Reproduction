import json
import os

from dotenv import load_dotenv

from chemcrow.agents import ChemCrow


def main():
    load_dotenv()
    chem_model = ChemCrow(
        model=os.environ["CHEMCROW_MODEL"],
        tools_model=os.environ["CHEMCROW_TOOLS_MODEL"],
        temp=0.0,
        max_iterations=10,
        streaming=False,
        verbose=True,
        openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base=os.environ["OPENAI_API_BASE"],
        api_keys={
            "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"],
            "OPENAI_API_BASE": os.environ["OPENAI_API_BASE"],
            "RXN4CHEM_API_KEY": os.environ["RXN4CHEM_API_KEY"],
            "RXN4CHEM_PROJECT_ID": os.environ["RXN4CHEM_PROJECT_ID"],
            "SERP_API_KEY": os.environ["SERP_API_KEY"],
            "CHEMCROW_SUMMARY_MODEL": os.environ["CHEMCROW_SUMMARY_MODEL"],
        },
    )
    question = (
        "What is the product of the reaction between styrene and dibromine? "
        "Answer briefly."
    )
    answer = chem_model.run(question)
    print(
        json.dumps(
            {
                "question": question,
                "answer": answer,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
