from recruiter_chat import understand_recruiter_query


queries = [
    "Who are the best candidates for this role?",
    "Compare Swetha R and Sathish Kumar",
    "Give me interview questions for Swetha R",
    "Show me the screening report",
    "Prioritize candidates with strong AWS experience",
]


for query in queries:

    result = understand_recruiter_query(query)

    print(
        f"\nQuery: {query}"
    )

    print(
        f"Intent: {result}"
    )