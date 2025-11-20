"""
Query validator to ensure only factual questions are answered
Refuses investment advice requests
"""

import re
from typing import Dict

class QueryValidator:
    """Validates user queries to ensure facts-only responses"""
    
    # Patterns that indicate investment advice requests
    ADVICE_PATTERNS = [
        r"should i (buy|invest|sell|redeem|switch)",
        r"is (it|this|now) (a )?good (time|idea|choice)",
        r"what (should|would) (you|i) (recommend|suggest|do)",
        r"(recommend|suggest|advice|opinion)",
        r"which (fund|scheme) (is|should) (best|better)",
        r"compare.*returns",
        r"performance.*vs",
        r"which one (to|should) (choose|pick|invest)"
    ]
    
    # Allowed factual question patterns
    FACTUAL_PATTERNS = [
        r"expense ratio",
        r"exit load",
        r"entry load",
        r"minimum (sip|investment|amount)",
        r"lock.?in",
        r"riskometer",
        r"benchmark",
        r"how to (download|get|access)",
        r"statement",
        r"factsheet",
        r"nav",
        r"fund manager",
        r"inception date",
        r"investment objective",
        r"portfolio",
        r"holdings"
    ]
    
    EDUCATIONAL_LINK = "https://mf.nipponindiaim.com/KnowledgeCenter/Pages/Investor-Education.aspx"
    
    def validate(self, query: str) -> Dict:
        """
        Validate query and return validation result
        Returns dict with is_valid, message, and optional educational_link
        """
        query_lower = query.lower().strip()
        
        # Check for advice patterns
        for pattern in self.ADVICE_PATTERNS:
            if re.search(pattern, query_lower):
                return {
                    "is_valid": False,
                    "message": "I provide factual information only, not investment advice. Please consult a registered financial advisor for investment decisions. Facts-only. No investment advice.",
                    "educational_link": self.EDUCATIONAL_LINK
                }
        
        # Check if it's a factual question
        is_factual = any(re.search(pattern, query_lower) for pattern in self.FACTUAL_PATTERNS)
        
        if not is_factual and len(query) > 10:
            # Might be a factual question but not matching patterns - allow it
            # But warn if it seems like advice
            if any(word in query_lower for word in ["should", "recommend", "advice", "opinion"]):
                return {
                    "is_valid": False,
                    "message": "I provide factual information only, not investment advice. Please consult a registered financial advisor for investment decisions. Facts-only. No investment advice.",
                    "educational_link": self.EDUCATIONAL_LINK
                }
        
        return {
            "is_valid": True,
            "message": ""
        }



