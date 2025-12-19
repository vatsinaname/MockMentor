
"""
Evaluation Rubrics for MockMentor
"""

RUBRICS = {
    "default": {
        "accuracy": {
            "weight": 0.5,
            "description": "Is the technical information factually correct? Does the code/query run?",
            "levels": {
                "high": "Completely correct, handles edge cases.",
                "medium": "Mostly correct, minor syntax or logic errors.",
                "low": "Fundamentally incorrect approach."
            }
        },
        "completeness": {
            "weight": 0.3,
            "description": "Did the candidate address all parts of the question? Did they explain the 'Why'?",
            "levels": {
                "high": "Comprehensive answer, includes trade-offs and reasoning.",
                "medium": "Answers the main point but misses nuance or alternative approaches.",
                "low": "Very brief or missing key components."
            }
        },
        "clarity": {
            "weight": 0.2,
            "description": "Is the explanation easy to follow? Is communication clear?",
            "levels": {
                "high": "Clear, structured, professional communication.",
                "medium": "Understandable but unstructured or rambling.",
                "low": "Confusing or difficult to parse."
            }
        }
    }
}
