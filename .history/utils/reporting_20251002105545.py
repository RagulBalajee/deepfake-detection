"""
User Reporting and Community Verification Module
Handles user reports and crowdsourced verification
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import asyncio

class CommunityReportingSystem:
    def __init__(self):
        self.user_reports = {}  # In production, use database
        self.community_verifications = {}  # In production, use database
        self.report_types = [
            "fake_news", "deepfake", "misinformation", "manipulation",
            "hate_speech", "spam", "copyright", "privacy_violation"
        ]
    
    async def submit_user_report(self, content_id: str, report_type: str, 
                               description: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Submit user report for suspicious content
        """
        try:
            if report_type not in self.report_types:
                return {
                    "success": False,
                    "error": f"Invalid report type. Must be one of: {', '.join(self.report_types)}"
                }
            
            report_id = f"report_{datetime.now().timestamp()}"
            
            report = {
                "report_id": report_id,
                "content_id": content_id,
                "report_type": report_type,
                "description": description,
                "user_id": user_id or "anonymous",
                "timestamp": datetime.now().isoformat(),
                "status": "pending",
                "community_votes": 0,
                "expert_review": False
            }
            
            # Store report
            if content_id not in self.user_reports:
                self.user_reports[content_id] = []
            
            self.user_reports[content_id].append(report)
            
            # Trigger community verification
            await self._trigger_community_verification(content_id, report)
            
            return {
                "success": True,
                "report_id": report_id,
                "message": "Report submitted successfully",
                "next_steps": "Community verification in progress"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Report submission failed: {str(e)}"
            }
    
    async def get_community_reports(self, content_id: str) -> Dict[str, Any]:
        """
        Get community reports for specific content
        """
        try:
            if content_id not in self.user_reports:
                return {
                    "content_id": content_id,
                    "reports": [],
                    "summary": {
                        "total_reports": 0,
                        "report_types": {},
                        "community_consensus": "no_reports"
                    }
                }
            
            reports = self.user_reports[content_id]
            
            # Analyze report types
            report_type_counts = {}
            for report in reports:
                report_type = report["report_type"]
                report_type_counts[report_type] = report_type_counts.get(report_type, 0) + 1
            
            # Calculate community consensus
            total_reports = len(reports)
            if total_reports == 0:
                consensus = "no_reports"
            elif total_reports >= 5:
                consensus = "high_concern"
            elif total_reports >= 3:
                consensus = "moderate_concern"
            else:
                consensus = "low_concern"
            
            return {
                "content_id": content_id,
                "reports": reports,
                "summary": {
                    "total_reports": total_reports,
                    "report_types": report_type_counts,
                    "community_consensus": consensus,
                    "latest_report": reports[-1]["timestamp"] if reports else None
                }
            }
            
        except Exception as e:
            return {
                "content_id": content_id,
                "error": f"Failed to retrieve reports: {str(e)}",
                "reports": [],
                "summary": {}
            }
    
    async def vote_on_report(self, report_id: str, vote: str, user_id: str) -> Dict[str, Any]:
        """
        Vote on community reports (like/dislike)
        """
        try:
            if vote not in ["upvote", "downvote"]:
                return {
                    "success": False,
                    "error": "Invalid vote. Must be 'upvote' or 'downvote'"
                }
            
            # Find report across all content
            report_found = False
            for content_id, reports in self.user_reports.items():
                for report in reports:
                    if report["report_id"] == report_id:
                        # Update vote count
                        if "votes" not in report:
                            report["votes"] = {"upvotes": 0, "downvotes": 0}
                        
                        if vote == "upvote":
                            report["votes"]["upvotes"] += 1
                        else:
                            report["votes"]["downvotes"] += 1
                        
                        report_found = True
                        break
                
                if report_found:
                    break
            
            if not report_found:
                return {
                    "success": False,
                    "error": "Report not found"
                }
            
            return {
                "success": True,
                "message": f"Vote {vote} recorded successfully",
                "report_id": report_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Voting failed: {str(e)}"
            }
    
    async def get_community_dashboard(self) -> Dict[str, Any]:
        """
        Get community reporting dashboard with statistics
        """
        try:
            total_reports = sum(len(reports) for reports in self.user_reports.values())
            
            # Calculate report type distribution
            all_reports = []
            for reports in self.user_reports.values():
                all_reports.extend(reports)
            
            report_type_distribution = {}
            for report in all_reports:
                report_type = report["report_type"]
                report_type_distribution[report_type] = report_type_distribution.get(report_type, 0) + 1
            
            # Calculate recent activity
            recent_reports = [
                report for reports in self.user_reports.values() 
                for report in reports
                if datetime.fromisoformat(report["timestamp"]) > datetime.now() - timedelta(days=7)
            ]
            
            return {
                "total_reports": total_reports,
                "recent_reports": len(recent_reports),
                "report_type_distribution": report_type_distribution,
                "top_reported_content": self._get_top_reported_content(),
                "community_engagement": self._calculate_community_engagement(),
                "dashboard_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Dashboard generation failed: {str(e)}",
                "total_reports": 0,
                "recent_reports": 0,
                "report_type_distribution": {},
                "top_reported_content": [],
                "community_engagement": 0
            }
    
    async def _trigger_community_verification(self, content_id: str, report: Dict[str, Any]):
        """Trigger community verification process"""
        # In production, this would notify community members
        # and start verification workflow
        pass
    
    def _get_top_reported_content(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most reported content"""
        content_report_counts = []
        
        for content_id, reports in self.user_reports.items():
            content_report_counts.append({
                "content_id": content_id,
                "report_count": len(reports),
                "latest_report": max(report["timestamp"] for report in reports) if reports else None
            })
        
        # Sort by report count and return top N
        content_report_counts.sort(key=lambda x: x["report_count"], reverse=True)
        return content_report_counts[:limit]
    
    def _calculate_community_engagement(self) -> float:
        """Calculate community engagement score"""
        if not self.user_reports:
            return 0.0
        
        total_reports = sum(len(reports) for reports in self.user_reports.values())
        unique_content = len(self.user_reports)
        
        # Engagement score based on reports per content
        if unique_content > 0:
            return min(total_reports / unique_content, 10.0)
        return 0.0

# Global instance
community_reporting = CommunityReportingSystem()

async def submit_user_report(content_id: str, report_type: str, 
                           description: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to submit user report
    """
    return await community_reporting.submit_user_report(content_id, report_type, description, user_id)

async def get_community_reports(content_id: str) -> Dict[str, Any]:
    """
    Main function to get community reports
    """
    return await community_reporting.get_community_reports(content_id)
