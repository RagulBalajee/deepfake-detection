"""
Psychological Impact Detector Module
Identifies manipulation strategies and psychological triggers in content
"""

import re
from typing import Dict, Any, List, Tuple
import json
from datetime import datetime

class PsychologicalImpactDetector:
    def __init__(self):
        # Emotional manipulation patterns
        self.emotional_triggers = {
            'fear': [
                'danger', 'threat', 'crisis', 'emergency', 'warning', 'alert',
                'scary', 'terrifying', 'frightening', 'alarming', 'shocking'
            ],
            'anger': [
                'outrage', 'infuriating', 'disgusting', 'appalling', 'unacceptable',
                'anger', 'furious', 'mad', 'upset', 'offended'
            ],
            'sadness': [
                'heartbreaking', 'tragic', 'devastating', 'sad', 'depressing',
                'mourning', 'grief', 'loss', 'suffering', 'pain'
            ],
            'joy': [
                'amazing', 'incredible', 'fantastic', 'wonderful', 'excellent',
                'celebrating', 'victory', 'success', 'breakthrough', 'miracle'
            ]
        }
        
        # Persuasion techniques
        self.persuasion_techniques = {
            'urgency': [
                'urgent', 'immediate', 'now', 'quickly', 'hurry', 'deadline',
                'limited time', 'act now', 'don\'t wait', 'expires soon'
            ],
            'authority': [
                'expert', 'scientist', 'doctor', 'professor', 'official',
                'government', 'study shows', 'research proves', 'according to'
            ],
            'social_proof': [
                'everyone', 'most people', 'studies show', 'statistics',
                'majority', 'popular', 'trending', 'viral', 'shared'
            ],
            'scarcity': [
                'rare', 'exclusive', 'limited', 'only', 'unique', 'special',
                'one of a kind', 'hard to find', 'unavailable', 'sold out'
            ]
        }
        
        # Cognitive bias indicators
        self.cognitive_biases = {
            'confirmation_bias': [
                'as expected', 'proves my point', 'told you so', 'exactly what i thought',
                'this confirms', 'as i suspected', 'no surprise'
            ],
            'availability_heuristic': [
                'recent', 'latest', 'breaking', 'just happened', 'current',
                'today', 'now', 'immediate', 'instant'
            ],
            'anchoring': [
                'first', 'original', 'initial', 'starting', 'beginning',
                'base', 'foundation', 'primary', 'main'
            ]
        }
    
    async def detect_psychological_impact(self, content: str) -> Dict[str, Any]:
        """
        Detect psychological manipulation and impact in content
        """
        try:
            content_lower = content.lower()
            
            # Analyze emotional triggers
            emotional_analysis = self._analyze_emotional_triggers(content_lower)
            
            # Analyze persuasion techniques
            persuasion_analysis = self._analyze_persuasion_techniques(content_lower)
            
            # Analyze cognitive biases
            bias_analysis = self._analyze_cognitive_biases(content_lower)
            
            # Calculate manipulation score
            manipulation_score = self._calculate_manipulation_score(
                emotional_analysis, persuasion_analysis, bias_analysis
            )
            
            # Determine manipulation intent
            manipulation_intent = self._determine_manipulation_intent(
                emotional_analysis, persuasion_analysis, bias_analysis
            )
            
            return {
                "manipulation_score": round(manipulation_score, 3),
                "manipulation_intent": manipulation_intent,
                "emotional_triggers": emotional_analysis,
                "persuasion_techniques": persuasion_analysis,
                "cognitive_biases": bias_analysis,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "manipulation_score": 0.0,
                "manipulation_intent": "unknown",
                "error": f"Psychological analysis failed: {str(e)}"
            }
    
    def _analyze_emotional_triggers(self, content: str) -> Dict[str, Any]:
        """Analyze emotional triggers in content"""
        emotional_scores = {}
        
        for emotion, triggers in self.emotional_triggers.items():
            matches = sum(1 for trigger in triggers if trigger in content)
            intensity = matches / len(triggers)
            
            emotional_scores[emotion] = {
                "matches": matches,
                "intensity": round(intensity, 3),
                "triggers_found": [trigger for trigger in triggers if trigger in content]
            }
        
        # Determine dominant emotion
        dominant_emotion = max(emotional_scores.items(), key=lambda x: x[1]["intensity"])
        
        return {
            "emotional_scores": emotional_scores,
            "dominant_emotion": dominant_emotion[0],
            "overall_emotional_intensity": dominant_emotion[1]["intensity"]
        }
    
    def _analyze_persuasion_techniques(self, content: str) -> Dict[str, Any]:
        """Analyze persuasion techniques used in content"""
        technique_scores = {}
        
        for technique, indicators in self.persuasion_techniques.items():
            matches = sum(1 for indicator in indicators if indicator in content)
            strength = matches / len(indicators)
            
            technique_scores[technique] = {
                "matches": matches,
                "strength": round(strength, 3),
                "indicators_found": [indicator for indicator in indicators if indicator in content]
            }
        
        # Calculate overall persuasion score
        total_techniques = sum(score["strength"] for score in technique_scores.values())
        overall_persuasion = total_techniques / len(technique_scores)
        
        return {
            "technique_scores": technique_scores,
            "overall_persuasion": round(overall_persuasion, 3)
        }
    
    def _analyze_cognitive_biases(self, content: str) -> Dict[str, Any]:
        """Analyze cognitive biases in content"""
        bias_scores = {}
        
        for bias, indicators in self.cognitive_biases.items():
            matches = sum(1 for indicator in indicators if indicator in content)
            strength = matches / len(indicators)
            
            bias_scores[bias] = {
                "matches": matches,
                "strength": round(strength, 3),
                "indicators_found": [indicator for indicator in indicators if indicator in content]
            }
        
        # Calculate overall bias score
        total_biases = sum(score["strength"] for score in bias_scores.values())
        overall_bias = total_biases / len(bias_scores)
        
        return {
            "bias_scores": bias_scores,
            "overall_bias": round(overall_bias, 3)
        }
    
    def _calculate_manipulation_score(self, emotional_analysis: Dict, 
                                    persuasion_analysis: Dict, 
                                    bias_analysis: Dict) -> float:
        """Calculate overall manipulation score"""
        # Weighted combination of different factors
        emotional_weight = 0.4
        persuasion_weight = 0.4
        bias_weight = 0.2
        
        emotional_score = emotional_analysis.get("overall_emotional_intensity", 0)
        persuasion_score = persuasion_analysis.get("overall_persuasion", 0)
        bias_score = bias_analysis.get("overall_bias", 0)
        
        manipulation_score = (
            emotional_score * emotional_weight +
            persuasion_score * persuasion_weight +
            bias_score * bias_weight
        )
        
        return min(manipulation_score, 1.0)
    
    def _determine_manipulation_intent(self, emotional_analysis: Dict,
                                      persuasion_analysis: Dict,
                                      bias_analysis: Dict) -> str:
        """Determine the likely manipulation intent"""
        emotional_intensity = emotional_analysis.get("overall_emotional_intensity", 0)
        persuasion_strength = persuasion_analysis.get("overall_persuasion", 0)
        bias_strength = bias_analysis.get("overall_bias", 0)
        
        # High manipulation indicators
        if emotional_intensity > 0.7 and persuasion_strength > 0.7:
            return "high_manipulation"
        elif emotional_intensity > 0.5 or persuasion_strength > 0.5:
            return "moderate_manipulation"
        elif bias_strength > 0.6:
            return "cognitive_bias"
        else:
            return "low_manipulation"

# Global instance
psychological_detector = PsychologicalImpactDetector()

async def detect_psychological_impact(content: str) -> Dict[str, Any]:
    """
    Main function to detect psychological impact and manipulation
    """
    return await psychological_detector.detect_psychological_impact(content)
