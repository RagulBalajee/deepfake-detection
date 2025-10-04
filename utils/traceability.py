"""
Cross-Platform Traceability Module
Tracks content spread across platforms and analyzes propagation patterns
"""

import re
import hashlib
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timedelta
import asyncio

class ContentTraceabilityTracker:
    def __init__(self):
        self.platform_patterns = {
            'twitter': r'twitter\.com|t\.co',
            'facebook': r'facebook\.com|fb\.com',
            'instagram': r'instagram\.com',
            'youtube': r'youtube\.com|youtu\.be',
            'reddit': r'reddit\.com',
            'telegram': r't\.me|telegram\.me',
            'whatsapp': r'whatsapp\.com|wa\.me',
            'tiktok': r'tiktok\.com',
            'linkedin': r'linkedin\.com'
        }
        
        self.content_hashes = {}  # In production, use database
        self.spread_networks = {}  # In production, use graph database
    
    async def track_content_spread(self, content: str, source_url: Optional[str] = None, 
                                 content_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Track content spread across platforms
        """
        try:
            if content_id:
                # Retrieve existing tracking data
                return await self._get_existing_tracking(content_id)
            
            # Generate content fingerprint
            content_hash = self._generate_content_hash(content)
            
            # Analyze source platform
            source_platform = self._identify_platform(source_url) if source_url else "unknown"
            
            # Simulate cross-platform detection (in production, use APIs)
            detected_platforms = await self._detect_cross_platform_presence(content_hash)
            
            # Analyze propagation patterns
            propagation_analysis = self._analyze_propagation_patterns(detected_platforms)
            
            # Generate spread map
            spread_map = self._generate_spread_map(source_platform, detected_platforms)
            
            # Calculate virality metrics
            virality_metrics = self._calculate_virality_metrics(detected_platforms)
            
            # Store tracking data
            tracking_data = {
                "content_hash": content_hash,
                "source_platform": source_platform,
                "detected_platforms": detected_platforms,
                "propagation_analysis": propagation_analysis,
                "spread_map": spread_map,
                "virality_metrics": virality_metrics,
                "tracking_timestamp": datetime.now().isoformat()
            }
            
            if content_id:
                self.content_hashes[content_id] = tracking_data
            
            return tracking_data
            
        except Exception as e:
            return {
                "error": f"Traceability tracking failed: {str(e)}",
                "content_hash": None,
                "source_platform": "unknown",
                "detected_platforms": [],
                "propagation_analysis": {},
                "spread_map": {},
                "virality_metrics": {}
            }
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate content fingerprint for tracking"""
        # Normalize content for consistent hashing
        normalized_content = re.sub(r'\s+', ' ', content.lower().strip())
        return hashlib.sha256(normalized_content.encode()).hexdigest()[:16]
    
    def _identify_platform(self, url: str) -> str:
        """Identify platform from URL"""
        if not url:
            return "unknown"
        
        url_lower = url.lower()
        for platform, pattern in self.platform_patterns.items():
            if re.search(pattern, url_lower):
                return platform
        
        return "unknown"
    
    async def _detect_cross_platform_presence(self, content_hash: str) -> List[Dict[str, Any]]:
        """
        Detect content presence across platforms
        In production, this would use platform APIs
        """
        # Simulate cross-platform detection
        platforms = [
            {
                "platform": "twitter",
                "detected": True,
                "confidence": 0.85,
                "first_seen": (datetime.now() - timedelta(hours=2)).isoformat(),
                "engagement": {"likes": 150, "retweets": 45, "replies": 23}
            },
            {
                "platform": "facebook",
                "detected": True,
                "confidence": 0.92,
                "first_seen": (datetime.now() - timedelta(hours=1)).isoformat(),
                "engagement": {"likes": 320, "shares": 89, "comments": 67}
            },
            {
                "platform": "reddit",
                "detected": True,
                "confidence": 0.78,
                "first_seen": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "engagement": {"upvotes": 45, "downvotes": 12, "comments": 23}
            }
        ]
        
        return platforms
    
    def _analyze_propagation_patterns(self, detected_platforms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how content propagated across platforms"""
        if not detected_platforms:
            return {"pattern": "no_detection", "speed": 0, "reach": 0}
        
        # Calculate propagation speed
        timestamps = [datetime.fromisoformat(p["first_seen"]) for p in detected_platforms if p.get("detected")]
        if len(timestamps) > 1:
            time_span = max(timestamps) - min(timestamps)
            speed = len(timestamps) / max(time_span.total_seconds() / 3600, 1)  # platforms per hour
        else:
            speed = 0
        
        # Calculate total reach
        total_engagement = sum(
            sum(p.get("engagement", {}).values()) for p in detected_platforms
        )
        
        # Determine propagation pattern
        if speed > 2:
            pattern = "viral"
        elif speed > 1:
            pattern = "rapid_spread"
        elif speed > 0.5:
            pattern = "moderate_spread"
        else:
            pattern = "slow_spread"
        
        return {
            "pattern": pattern,
            "speed": round(speed, 2),
            "reach": total_engagement,
            "platforms_count": len(detected_platforms)
        }
    
    def _generate_spread_map(self, source_platform: str, detected_platforms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate visual spread map data"""
        nodes = []
        edges = []
        
        # Add source node
        nodes.append({
            "id": source_platform,
            "type": "source",
            "platform": source_platform,
            "size": 20
        })
        
        # Add detected platform nodes
        for platform_data in detected_platforms:
            if platform_data.get("detected"):
                platform = platform_data["platform"]
                nodes.append({
                    "id": platform,
                    "type": "detected",
                    "platform": platform,
                    "size": platform_data.get("confidence", 0.5) * 30,
                    "engagement": platform_data.get("engagement", {})
                })
                
                # Add edge from source to detected platform
                edges.append({
                    "source": source_platform,
                    "target": platform,
                    "strength": platform_data.get("confidence", 0.5)
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "force_directed"
        }
    
    def _calculate_virality_metrics(self, detected_platforms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate virality metrics"""
        if not detected_platforms:
            return {"virality_score": 0, "risk_level": "low"}
        
        # Calculate virality score
        total_engagement = sum(
            sum(p.get("engagement", {}).values()) for p in detected_platforms
        )
        
        avg_confidence = sum(p.get("confidence", 0) for p in detected_platforms) / len(detected_platforms)
        
        virality_score = (total_engagement / 1000) * avg_confidence
        
        # Determine risk level
        if virality_score > 0.8:
            risk_level = "high"
        elif virality_score > 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "virality_score": round(virality_score, 3),
            "risk_level": risk_level,
            "total_engagement": total_engagement,
            "platforms_reached": len(detected_platforms)
        }
    
    async def _get_existing_tracking(self, content_id: str) -> Dict[str, Any]:
        """Get existing tracking data for content"""
        if content_id in self.content_hashes:
            return self.content_hashes[content_id]
        else:
            return {
                "error": "Content not found",
                "content_hash": None,
                "source_platform": "unknown",
                "detected_platforms": [],
                "propagation_analysis": {},
                "spread_map": {},
                "virality_metrics": {}
            }

# Global instance
traceability_tracker = ContentTraceabilityTracker()

async def track_content_spread(content: str, source_url: Optional[str] = None, 
                             content_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to track content spread across platforms
    """
    return await traceability_tracker.track_content_spread(content, source_url, content_id)
