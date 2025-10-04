"""
Source Credibility Scoring Module
AI-based trust scoring for publishers, accounts, and sources
"""

import re
import requests
from urllib.parse import urlparse
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timedelta

class CredibilityScorer:
    def __init__(self):
        self.trusted_domains = [
            'bbc.com', 'reuters.com', 'ap.org', 'npr.org',
            'nytimes.com', 'washingtonpost.com', 'theguardian.com',
            'factcheck.org', 'politifact.com', 'snopes.com'
        ]
        
        self.suspicious_domains = [
            'fake-news', 'conspiracy', 'hoax', 'satire'
        ]
        
        self.credibility_indicators = {
            'author_bio': 0.3,
            'publishing_date': 0.2,
            'source_attribution': 0.25,
            'fact_checking': 0.25
        }
    
    async def calculate_credibility_score(self, source_url: Optional[str] = None, 
                                        publisher: Optional[str] = None,
                                        author: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive credibility score for a source
        """
        try:
            if not source_url and not publisher:
                return {"credibility_score": 0.5, "confidence": 0.0, "details": "No source information provided"}
            
            # Analyze domain credibility
            domain_score = self._analyze_domain_credibility(source_url) if source_url else 0.5
            
            # Analyze publisher credibility
            publisher_score = self._analyze_publisher_credibility(publisher) if publisher else 0.5
            
            # Analyze author credibility
            author_score = self._analyze_author_credibility(author) if author else 0.5
            
            # Calculate weighted average
            weights = [0.4, 0.3, 0.3]  # Domain, Publisher, Author
            scores = [domain_score, publisher_score, author_score]
            
            overall_score = sum(w * s for w, s in zip(weights, scores))
            
            # Calculate confidence based on available information
            confidence = self._calculate_confidence(source_url, publisher, author)
            
            # Get detailed breakdown
            details = self._get_credibility_details(domain_score, publisher_score, author_score, source_url)
            
            return {
                "credibility_score": round(overall_score, 3),
                "confidence": round(confidence, 3),
                "domain_score": round(domain_score, 3),
                "publisher_score": round(publisher_score, 3),
                "author_score": round(author_score, 3),
                "details": details,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "credibility_score": 0.5,
                "confidence": 0.0,
                "error": f"Credibility analysis failed: {str(e)}"
            }
    
    def _analyze_domain_credibility(self, url: str) -> float:
        """Analyze domain credibility based on URL"""
        if not url:
            return 0.5
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Check against trusted domains
            for trusted_domain in self.trusted_domains:
                if trusted_domain in domain:
                    return 0.9
            
            # Check against suspicious domains
            for suspicious_domain in self.suspicious_domains:
                if suspicious_domain in domain:
                    return 0.1
            
            # Check for HTTPS
            if parsed_url.scheme == 'https':
                score = 0.6
            else:
                score = 0.3
            
            # Check for subdomain patterns (news sites often have specific patterns)
            if 'news' in domain or 'media' in domain:
                score += 0.1
            
            # Check for government domains
            if domain.endswith('.gov') or domain.endswith('.edu'):
                score = 0.8
            
            return min(score, 1.0)
            
        except Exception:
            return 0.5
    
    def _analyze_publisher_credibility(self, publisher: str) -> float:
        """Analyze publisher credibility"""
        if not publisher:
            return 0.5
        
        publisher_lower = publisher.lower()
        
        # Known credible publishers
        credible_publishers = [
            'bbc', 'reuters', 'associated press', 'npr', 'new york times',
            'washington post', 'guardian', 'wall street journal'
        ]
        
        for credible in credible_publishers:
            if credible in publisher_lower:
                return 0.9
        
        # Check for suspicious indicators
        suspicious_indicators = ['fake', 'satire', 'parody', 'hoax', 'conspiracy']
        for indicator in suspicious_indicators:
            if indicator in publisher_lower:
                return 0.2
        
        # Default score for unknown publishers
        return 0.5
    
    def _analyze_author_credibility(self, author: str) -> float:
        """Analyze author credibility"""
        if not author:
            return 0.5
        
        author_lower = author.lower()
        
        # Check for professional indicators
        professional_indicators = ['reporter', 'journalist', 'correspondent', 'editor']
        professional_score = sum(1 for indicator in professional_indicators if indicator in author_lower)
        
        if professional_score > 0:
            return 0.8
        
        # Check for suspicious indicators
        suspicious_indicators = ['anonymous', 'unknown', 'fake', 'bot']
        for indicator in suspicious_indicators:
            if indicator in author_lower:
                return 0.2
        
        # Default score for unknown authors
        return 0.5
    
    def _calculate_confidence(self, source_url: Optional[str], publisher: Optional[str], author: Optional[str]) -> float:
        """Calculate confidence in credibility assessment"""
        available_info = sum([
            1 if source_url else 0,
            1 if publisher else 0,
            1 if author else 0
        ])
        
        return available_info / 3.0
    
    def _get_credibility_details(self, domain_score: float, publisher_score: float, 
                               author_score: float, source_url: Optional[str]) -> Dict[str, Any]:
        """Get detailed credibility breakdown"""
        details = {
            "domain_analysis": {
                "score": domain_score,
                "url": source_url,
                "assessment": self._get_score_assessment(domain_score)
            },
            "publisher_analysis": {
                "score": publisher_score,
                "assessment": self._get_score_assessment(publisher_score)
            },
            "author_analysis": {
                "score": author_score,
                "assessment": self._get_score_assessment(author_score)
            }
        }
        
        return details
    
    def _get_score_assessment(self, score: float) -> str:
        """Get human-readable assessment of score"""
        if score >= 0.8:
            return "Highly Credible"
        elif score >= 0.6:
            return "Moderately Credible"
        elif score >= 0.4:
            return "Low Credibility"
        else:
            return "Very Low Credibility"

# Global instance
credibility_scorer = CredibilityScorer()

async def calculate_credibility_score(source_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to calculate credibility score
    """
    return await credibility_scorer.calculate_credibility_score(source_url)
