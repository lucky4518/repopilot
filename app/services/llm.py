import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def get_llm():

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "OPENROUTER_API_KEY is not set."
        )

    return ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct",
        temperature=0,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )