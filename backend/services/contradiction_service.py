from typing import List, Dict, Any

class ContradictionService:
    @staticmethod
    def classify_contradiction_severity(relationship: str, human_review: bool) -> str:
        """Helper to classify review priority for UI badges."""
        if relationship == "Potential Contradiction":
            return "high"
        elif relationship == "Difference":
            return "medium"
        elif relationship == "Agreement":
            return "low"
        return "neutral"
