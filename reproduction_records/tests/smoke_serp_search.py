import json
import os

from dotenv import load_dotenv
from serpapi import GoogleSearch


def main():
    load_dotenv()
    search = GoogleSearch(
        {
            "q": "acetaminophen molecular weight",
            "api_key": os.environ["SERP_API_KEY"],
            "num": 3,
        }
    )
    results = search.get_dict()
    organic = results.get("organic_results", [])
    print(
        json.dumps(
            {
                "organic_count": len(organic),
                "first_title": organic[0].get("title") if organic else None,
                "first_link": organic[0].get("link") if organic else None,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
