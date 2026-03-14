import json
import os
from time import sleep

from dotenv import load_dotenv

from chemcrow.tools.rxn4chem import RXNRetrosynthesis


def main():
    load_dotenv()
    sleep(2)
    tool = RXNRetrosynthesis(
        os.environ["RXN4CHEM_API_KEY"],
        os.environ["OPENAI_API_KEY"],
        project_id=os.environ["RXN4CHEM_PROJECT_ID"],
        summary_model=os.environ["CHEMCROW_SUMMARY_MODEL"],
        openai_api_base=os.environ["OPENAI_API_BASE"],
    )
    target = "CC(=O)Oc1ccccc1C(=O)O"
    prediction_id = None
    path_count = None
    stage = "init"
    try:
        stage = "predict_retrosynthesis"
        prediction_id = tool.predict_retrosynthesis(target)
        stage = "get_paths"
        paths = tool.get_paths(prediction_id)
        path_count = len(paths) if isinstance(paths, list) else None
        stage = "get_action_sequence"
        result = tool.get_action_sequence(paths[0])
        error = None
    except Exception as exc:
        result = None
        error = f"{type(exc).__name__}: {exc}"
    print(
        json.dumps(
            {
                "target": target,
                "prediction_id": prediction_id,
                "path_count": path_count,
                "stage": stage,
                "result": result,
                "error": error,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
