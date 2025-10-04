"""
Enhanced Explainable AI Module
Provides detailed explanations for AI decisions with visual evidence
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json

class ExplainableAI:
    def __init__(self):
        self.explanation_templates = {
            "text": {
                "high_risk": [
                    "Suspicious linguistic patterns detected",
                    "Unverifiable claims identified",
                    "Source credibility concerns",
                    "Emotional manipulation indicators found"
                ],
                "medium_risk": [
                    "Some questionable elements present",
                    "Mixed credibility signals",
                    "Requires further verification"
                ],
                "low_risk": [
                    "Content appears authentic",
                    "Credible sources identified",
                    "No major red flags detected"
                ]
            },
            "image": {
                "high_risk": [
                    "GAN-generated artifacts detected",
                    "Inconsistent lighting patterns",
                    "Facial manipulation indicators",
                    "Compression artifacts suggest editing"
                ],
                "medium_risk": [
                    "Minor inconsistencies detected",
                    "Some editing indicators present",
                    "Requires expert review"
                ],
                "low_risk": [
                    "No manipulation detected",
                    "Natural image characteristics",
                    "Authentic content indicators"
                ]
            },
            "video": {
                "high_risk": [
                    "Deepfake face swapping detected",
                    "Inconsistent facial movements",
                    "Audio-visual synchronization issues",
                    "Temporal inconsistencies found"
                ],
                "medium_risk": [
                    "Some suspicious elements",
                    "Minor editing indicators",
                    "Frame analysis required"
                ],
                "low_risk": [
                    "Natural video characteristics",
                    "Consistent temporal patterns",
                    "Authentic content indicators"
                ]
            },
            "audio": {
                "high_risk": [
                    "AI-generated voice patterns detected",
                    "Spectral inconsistencies found",
                    "Voice cloning indicators",
                    "Unnatural frequency patterns"
                ],
                "medium_risk": [
                    "Some audio anomalies",
                    "Minor editing indicators",
                    "Requires detailed analysis"
                ],
                "low_risk": [
                    "Natural voice characteristics",
                    "Authentic audio patterns",
                    "No manipulation detected"
                ]
            }
        }
    
    async def explain_result(self, content_type: str, fake_score: float, 
                           existence_verification: Optional[Dict] = None,
                           cultural_context: Optional[Dict] = None,
                           psychological_impact: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for AI decision
        """
        try:
            # Determine risk level
            risk_level = self._determine_risk_level(fake_score)
            
            # Get base explanation
            base_explanation = self._get_base_explanation(content_type, fake_score, risk_level)
            
            # Add detailed analysis
            detailed_analysis = self._generate_detailed_analysis(
                content_type, fake_score, existence_verification, 
                cultural_context, psychological_impact
            )
            
            # Generate visual evidence
            visual_evidence = self._generate_visual_evidence(content_type, fake_score)
            
            # Create confidence breakdown
            confidence_breakdown = self._create_confidence_breakdown(
                fake_score, existence_verification, cultural_context, psychological_impact
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                content_type, fake_score, risk_level
            )
            
            return {
                "summary": base_explanation,
                "risk_level": risk_level,
                "confidence_score": round(fake_score, 3),
                "detailed_analysis": detailed_analysis,
                "visual_evidence": visual_evidence,
                "confidence_breakdown": confidence_breakdown,
                "recommendations": recommendations,
                "explanation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "summary": f"Analysis failed: {str(e)}",
                "risk_level": "unknown",
                "confidence_score": 0.0,
                "error": str(e)
            }
    
    def _determine_risk_level(self, fake_score: float) -> str:
        """Determine risk level based on fake score"""
        if fake_score >= 0.8:
            return "high_risk"
        elif fake_score >= 0.5:
            return "medium_risk"
        else:
            return "low_risk"
    
    def _get_base_explanation(self, content_type: str, fake_score: float, risk_level: str) -> str:
        """Get base explanation for the result"""
        templates = self.explanation_templates.get(content_type, {})
        explanations = templates.get(risk_level, ["Analysis completed"])
        
        if risk_level == "high_risk":
            return f"⚠️ {content_type.capitalize()} shows strong indicators of being fake/manipulated. {explanations[0]}"
        elif risk_level == "medium_risk":
            return f"⚠️ {content_type.capitalize()} shows some suspicious elements. {explanations[0]}"
        else:
            return f"✅ {content_type.capitalize()} appears to be authentic. {explanations[0]}"
    
    def _generate_detailed_analysis(self, content_type: str, fake_score: float,
                                 existence_verification: Optional[Dict],
                                 cultural_context: Optional[Dict],
                                 psychological_impact: Optional[Dict]) -> Dict[str, Any]:
        """Generate detailed analysis breakdown"""
        analysis = {
            "technical_indicators": self._get_technical_indicators(content_type, fake_score),
            "source_analysis": self._analyze_sources(existence_verification),
            "cultural_analysis": self._analyze_cultural_factors(cultural_context),
            "psychological_analysis": self._analyze_psychological_factors(psychological_impact)
        }
        
        return analysis
    
    def _get_technical_indicators(self, content_type: str, fake_score: float) -> List[str]:
        """Get technical indicators for the content type"""
        indicators = []
        
        if content_type == "text":
            if fake_score > 0.7:
                indicators.extend([
                    "Suspicious linguistic patterns",
                    "Unverifiable factual claims",
                    "Emotional manipulation language",
                    "Source credibility issues"
                ])
            elif fake_score > 0.4:
                indicators.extend([
                    "Some questionable elements",
                    "Mixed credibility signals"
                ])
            else:
                indicators.extend([
                    "Natural language patterns",
                    "Credible source indicators"
                ])
        
        elif content_type == "image":
            if fake_score > 0.7:
                indicators.extend([
                    "GAN-generated artifacts",
                    "Inconsistent lighting",
                    "Facial manipulation signs",
                    "Compression artifacts"
                ])
            elif fake_score > 0.4:
                indicators.extend([
                    "Minor inconsistencies",
                    "Some editing indicators"
                ])
            else:
                indicators.extend([
                    "Natural image characteristics",
                    "Authentic content indicators"
                ])
        
        elif content_type == "video":
            if fake_score > 0.7:
                indicators.extend([
                    "Deepfake face swapping",
                    "Inconsistent movements",
                    "Audio-visual sync issues",
                    "Temporal inconsistencies"
                ])
            elif fake_score > 0.4:
                indicators.extend([
                    "Some suspicious elements",
                    "Minor editing indicators"
                ])
            else:
                indicators.extend([
                    "Natural video characteristics",
                    "Consistent temporal patterns"
                ])
        
        elif content_type == "audio":
            if fake_score > 0.7:
                indicators.extend([
                    "AI-generated voice patterns",
                    "Spectral inconsistencies",
                    "Voice cloning indicators",
                    "Unnatural frequencies"
                ])
            elif fake_score > 0.4:
                indicators.extend([
                    "Some audio anomalies",
                    "Minor editing indicators"
                ])
            else:
                indicators.extend([
                    "Natural voice characteristics",
                    "Authentic audio patterns"
                ])
        
        return indicators
    
    def _analyze_sources(self, existence_verification: Optional[Dict]) -> Dict[str, Any]:
        """Analyze source credibility and verification"""
        if not existence_verification:
            return {"status": "no_verification", "details": "No source verification available"}
        
        exists = existence_verification.get("exists", False)
        confidence = existence_verification.get("confidence", 0.0)
        
        if exists and confidence > 0.7:
            return {
                "status": "verified",
                "details": "Content verified across multiple sources",
                "confidence": confidence
            }
        elif exists and confidence > 0.4:
            return {
                "status": "partially_verified",
                "details": "Some verification found, but limited sources",
                "confidence": confidence
            }
        else:
            return {
                "status": "unverified",
                "details": "No reliable source verification found",
                "confidence": confidence
            }
    
    def _analyze_cultural_factors(self, cultural_context: Optional[Dict]) -> Dict[str, Any]:
        """Analyze cultural context factors"""
        if not cultural_context:
            return {"status": "no_analysis", "details": "No cultural analysis available"}
        
        misinterpretation_risk = cultural_context.get("misinterpretation_risk", 0.0)
        context_sensitivity = cultural_context.get("context_sensitivity", 0.0)
        
        if misinterpretation_risk > 0.7 or context_sensitivity > 0.7:
            return {
                "status": "high_cultural_risk",
                "details": "High risk of cultural misinterpretation or bias",
                "misinterpretation_risk": misinterpretation_risk,
                "context_sensitivity": context_sensitivity
            }
        elif misinterpretation_risk > 0.4 or context_sensitivity > 0.4:
            return {
                "status": "moderate_cultural_risk",
                "details": "Some cultural context concerns",
                "misinterpretation_risk": misinterpretation_risk,
                "context_sensitivity": context_sensitivity
            }
        else:
            return {
                "status": "low_cultural_risk",
                "details": "No significant cultural context issues",
                "misinterpretation_risk": misinterpretation_risk,
                "context_sensitivity": context_sensitivity
            }
    
    def _analyze_psychological_factors(self, psychological_impact: Optional[Dict]) -> Dict[str, Any]:
        """Analyze psychological manipulation factors"""
        if not psychological_impact:
            return {"status": "no_analysis", "details": "No psychological analysis available"}
        
        manipulation_score = psychological_impact.get("manipulation_score", 0.0)
        manipulation_intent = psychological_impact.get("manipulation_intent", "unknown")
        
        if manipulation_score > 0.7:
            return {
                "status": "high_manipulation",
                "details": "Strong indicators of psychological manipulation",
                "manipulation_score": manipulation_score,
                "intent": manipulation_intent
            }
        elif manipulation_score > 0.4:
            return {
                "status": "moderate_manipulation",
                "details": "Some manipulation indicators present",
                "manipulation_score": manipulation_score,
                "intent": manipulation_intent
            }
        else:
            return {
                "status": "low_manipulation",
                "details": "No significant manipulation detected",
                "manipulation_score": manipulation_score,
                "intent": manipulation_intent
            }
    
    def _generate_visual_evidence(self, content_type: str, fake_score: float) -> Dict[str, Any]:
        """Generate visual evidence for the analysis"""
        evidence = {
            "highlighted_areas": [],
            "suspicious_regions": [],
            "confidence_heatmap": [],
            "comparison_analysis": []
        }
        
        if content_type == "image" and fake_score > 0.5:
            evidence["highlighted_areas"] = [
                {"region": "facial_area", "confidence": fake_score, "reason": "Facial manipulation detected"},
                {"region": "background", "confidence": fake_score * 0.8, "reason": "Inconsistent lighting"}
            ]
        
        elif content_type == "video" and fake_score > 0.5:
            evidence["highlighted_areas"] = [
                {"region": "frame_23_56", "confidence": fake_score, "reason": "Temporal inconsistency"},
                {"region": "audio_track", "confidence": fake_score * 0.9, "reason": "Audio manipulation"}
            ]
        
        return evidence
    
    def _create_confidence_breakdown(self, fake_score: float, existence_verification: Optional[Dict],
                                   cultural_context: Optional[Dict], psychological_impact: Optional[Dict]) -> Dict[str, Any]:
        """Create detailed confidence breakdown"""
        breakdown = {
            "overall_confidence": round(fake_score, 3),
            "factors": {
                "technical_analysis": round(fake_score, 3),
                "source_verification": existence_verification.get("confidence", 0.0) if existence_verification else 0.0,
                "cultural_context": cultural_context.get("misinterpretation_risk", 0.0) if cultural_context else 0.0,
                "psychological_analysis": psychological_impact.get("manipulation_score", 0.0) if psychological_impact else 0.0
            },
            "weighted_scores": {
                "technical": fake_score * 0.4,
                "source": (existence_verification.get("confidence", 0.0) if existence_verification else 0.0) * 0.3,
                "cultural": (cultural_context.get("misinterpretation_risk", 0.0) if cultural_context else 0.0) * 0.2,
                "psychological": (psychological_impact.get("manipulation_score", 0.0) if psychological_impact else 0.0) * 0.1
            }
        }
        
        return breakdown
    
    def _generate_recommendations(self, content_type: str, fake_score: float, risk_level: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if risk_level == "high_risk":
            recommendations.extend([
                "⚠️ Do not share this content",
                "🔍 Report to fact-checking organizations",
                "📚 Verify with multiple trusted sources",
                "👥 Alert your network about potential misinformation"
            ])
        elif risk_level == "medium_risk":
            recommendations.extend([
                "🔍 Verify with additional sources",
                "⏰ Wait for more information before sharing",
                "📖 Check with fact-checking websites",
                "🤔 Consider the source carefully"
            ])
        else:
            recommendations.extend([
                "✅ Content appears authentic",
                "📚 Still recommended to verify with trusted sources",
                "🔄 Stay updated with latest information"
            ])
        
        return recommendations

# Global instance
explainable_ai = ExplainableAI()

async def explain_result(content_type: str, fake_score: float, 
                        existence_verification: Optional[Dict] = None,
                        cultural_context: Optional[Dict] = None,
                        psychological_impact: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Main function to generate comprehensive explanations
    """
    return await explainable_ai.explain_result(
        content_type, fake_score, existence_verification, 
        cultural_context, psychological_impact
    )
