from graphviz import Digraph


graph = Digraph(
    "Resume Matching Agent",
    format="png"
)

graph.attr(
    rankdir="TB",
    label="AI Resume Matching Agent - LangGraph Workflow",
    labelloc="t",
    fontsize="20"
)

graph.attr(
    "node",
    shape="box",
    style="rounded",
    fontsize="12"
)


# --------------------------------------------------
# Main workflow
# --------------------------------------------------

graph.node("start", "START", shape="ellipse")

graph.node(
    "parse_jd",
    "Parse JD"
)

graph.node(
    "extract",
    "Extract Requirements\n(Must-have / Nice-to-have)"
)

graph.node(
    "search",
    "Search Resumes\n(RAG + ChromaDB)"
)

graph.node(
    "rank",
    "Rank Candidates\n(Hybrid Matching)"
)

graph.node(
    "report",
    "Generate Screening Report"
)

graph.node(
    "feedback",
    "Human Feedback"
)

graph.node(
    "apply_feedback",
    "Apply Feedback\n& Update Requirements"
)

graph.node(
    "deep",
    "Round 2:\nDeep Screening"
)

graph.node(
    "final",
    "Round 3:\nFinal HIRE / NO HIRE"
)

graph.node(
    "end",
    "END",
    shape="ellipse"
)


# --------------------------------------------------
# Main edges
# --------------------------------------------------

graph.edge(
    "start",
    "parse_jd"
)

graph.edge(
    "parse_jd",
    "extract"
)

graph.edge(
    "extract",
    "search"
)

graph.edge(
    "search",
    "rank"
)

graph.edge(
    "rank",
    "report"
)

graph.edge(
    "report",
    "feedback"
)


# --------------------------------------------------
# Human feedback loop
# --------------------------------------------------

graph.edge(
    "feedback",
    "deep",
    label=" No feedback"
)

graph.edge(
    "feedback",
    "apply_feedback",
    label=" Feedback"
)

graph.edge(
    "apply_feedback",
    "extract",
    label=" Re-run matching"
)


# --------------------------------------------------
# Multi-round screening
# --------------------------------------------------

graph.edge(
    "deep",
    "final"
)

graph.edge(
    "final",
    "end"
)


# --------------------------------------------------
# Generate image
# --------------------------------------------------

output_path = graph.render(
    "agent_graph",
    cleanup=True
)

print(
    f"Agent graph generated successfully:\n{output_path}"
)