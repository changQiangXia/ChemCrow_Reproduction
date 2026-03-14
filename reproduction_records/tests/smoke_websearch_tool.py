import json
import os

from dotenv import load_dotenv

from chemcrow.tools.search import WebSearch


def main():
    load_dotenv()
    tool = WebSearch(os.environ["SERP_API_KEY"])
    query = "What is the molecular weight of acetaminophen?"
    result = tool._run(query)
    print(
        json.dumps(
            {
                "query": query,
                "result": result,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
