"""
Cultural Context Understanding Module
Analyzes content for cultural bias, regional misinterpretation, and context sensitivity
"""

import re
import json
from typing import Dict, Any, Optional
import requests
from datetime import datetime

class CulturalContextAnalyzer:
    def __init__(self):
        self.cultural_keywords = {
            'western': ['democracy', 'freedom', 'individual', 'capitalism'],
            'eastern': ['harmony', 'collective', 'tradition', 'respect'],
            'religious': ['god', 'prayer', 'faith', 'sacred'],
            'political': ['government', 'election', 'policy', 'vote']
        }
        
        self.regional_biases = {
            'us': ['america', 'usa', 'united states'],
            'uk': ['britain', 'england', 'london'],
            'india': ['india', 'hindi', 'bharat'],
            'china': ['china', 'chinese', 'beijing']
        }
    
    async def analyze_cultural_context(self, content: str, language: str = "en") -> Dict[str, Any]:
        """
        Analyze content for cultural context and potential bias
        """
        try:
            # Detect cultural indicators
            cultural_indicators = self._detect_cultural_indicators(content)
            
            # Analyze regional bias
            regional_bias = self._analyze_regional_bias(content)
            
            # Check for cultural misinterpretation
            misinterpretation_risk = self._assess_misinterpretation_risk(content, language)
            
            # Analyze context sensitivity
            context_sensitivity = self._analyze_context_sensitivity(content)
            
            return {
                "cultural_indicators": cultural_indicators,
                "regional_bias": regional_bias,
                "misinterpretation_risk": misinterpretation_risk,
                "context_sensitivity": context_sensitivity,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Cultural context analysis failed: {str(e)}",
                "cultural_indicators": {},
                "regional_bias": {},
                "misinterpretation_risk": 0.0,
                "context_sensitivity": 0.0
            }
    
    def _detect_cultural_indicators(self, content: str) -> Dict[str, Any]:
        """Detect cultural indicators in content"""
        indicators = {}
        content_lower = content.lower()
        
        for culture, keywords in self.cultural_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            indicators[culture] = {
                "matches": matches,
                "strength": matches / len(keywords),
                "keywords_found": [kw for kw in keywords if kw in content_lower]
            }
        
        return indicators
    
    def _analyze_regional_bias(self, content: str) -> Dict[str, Any]:
        """Analyze for regional bias in content"""
        content_lower = content.lower()
        bias_scores = {}
        
        for region, keywords in self.regional_biases.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            bias_scores[region] = {
                "matches": matches,
                "bias_strength": matches / len(keywords),
                "keywords_found": [kw for kw in keywords if kw in content_lower]
            }
        
        # Determine dominant regional bias
        dominant_bias = max(bias_scores.items(), key=lambda x: x[1]["bias_strength"])
        
        return {
            "regional_scores": bias_scores,
            "dominant_bias": dominant_bias[0],
            "bias_confidence": dominant_bias[1]["bias_strength"]
        }
    
    def _assess_misinterpretation_risk(self, content: str, language: str) -> float:
        """Assess risk of cultural misinterpretation"""
        risk_factors = 0
        total_factors = 4
        
        # Check for cultural references that might be misunderstood
        cultural_references = [
            'meme', 'joke', 'sarcasm', 'irony', 'satire',
            'tradition', 'custom', 'ritual', 'ceremony'
        ]
        
        content_lower = content.lower()
        cultural_refs_found = sum(1 for ref in cultural_references if ref in content_lower)
        if cultural_refs_found > 0:
            risk_factors += 1
        
        # Check for language-specific idioms
        if language != 'en':
            # Non-English content has higher misinterpretation risk
            risk_factors += 1
        
        # Check for emotional language that might be culturally sensitive
        emotional_words = ['offensive', 'disrespectful', 'inappropriate', 'wrong']
        if any(word in content_lower for word in emotional_words):
            risk_factors += 1
        
        # Check for historical or religious references
        sensitive_topics = ['war', 'religion', 'politics', 'history', 'tradition']
        if any(topic in content_lower for topic in sensitive_topics):
            risk_factors += 1
        
        return risk_factors / total_factors
    
    def _analyze_context_sensitivity(self, content: str) -> float:
        """Analyze how context-sensitive the content is"""
        sensitivity_indicators = [
            'out of context', 'misleading', 'misrepresented',
            'taken out of context', 'misunderstood', 'misinterpreted'
        ]
        
        content_lower = content.lower()
        sensitivity_score = sum(1 for indicator in sensitivity_indicators if indicator in content_lower)
        
        # Normalize to 0-1 scale
        return min(sensitivity_score / len(sensitivity_indicators), 1.0)

# Global instance
cultural_analyzer = CulturalContextAnalyzer()

async def analyze_cultural_context(content: str, language: str = "en") -> Dict[str, Any]:
    """
    Main function to analyze cultural context of content
    """
    return await cultural_analyzer.analyze_cultural_context(content, language)
