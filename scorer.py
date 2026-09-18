"""
Small evaluation scorer for the Unit 2 test runs.

The scorer checks whether the expected phrase from questions.py appears in
the generated answer. This makes Criterion 5 repeatable, but it is intentionally
limited: a substring match cannot prove that the entire answer is correct, and
a correct answer could theoretically use different wording.

Other acceptance criteria still require evidence from retrieval results,
source citations, the relevance gate, or manual chunk inspection.
"""


def judge(question, expects, answer, results) -> bool:
    """Return True when the expected phrase appears in the answer."""
    return expects.lower() in answer.lower()
    