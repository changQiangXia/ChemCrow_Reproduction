import json
import os

from dotenv import load_dotenv
from openai import ChatCompletion


def main():
    load_dotenv()
    response = ChatCompletion.create(
        api_key=os.environ["OPENAI_API_KEY"],
        api_base=os.environ["OPENAI_API_BASE"],
        model=os.environ["CHEMCROW_MODEL"],
        messages=[
            {
                "role": "user",
                "content": "Reply with the exact string CHEMCROW_QWEN_OK.",
            }
        ],
        temperature=0,
        max_tokens=32,
    )
    print(
        json.dumps(
            {
                "model": response["model"],
                "message": response["choices"][0]["message"]["content"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
