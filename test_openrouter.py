from langchain_openrouter import ChatOpenRouter
from src.config import OPENROUTER_MODEL


def main():
    print("Testing OpenRouter...")

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    response = model.invoke(
        "Explain in one sentence what RAG means."
    )

    print("\nOpenRouter Response:")
    print(response.content)


if __name__ == "__main__":
    main()