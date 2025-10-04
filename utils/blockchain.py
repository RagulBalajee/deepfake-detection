"""
Blockchain-Based Verification Module
Stores and verifies content hashes on blockchain for authenticity
"""

import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

class BlockchainVerifier:
    def __init__(self):
        # In production, this would connect to actual blockchain
        self.content_registry = {}  # Simulated blockchain storage
        self.verification_history = {}  # Track verification attempts
    
    async def store_content_hash(self, content: str, content_id: str) -> str:
        """
        Store content hash on blockchain for verification
        """
        try:
            # Generate content hash
            content_hash = self._generate_content_hash(content)
            
            # Create blockchain entry
            blockchain_entry = {
                "content_id": content_id,
                "content_hash": content_hash,
                "timestamp": datetime.now().isoformat(),
                "block_number": self._get_next_block_number(),
                "verified": True,
                "metadata": {
                    "content_length": len(content),
                    "hash_algorithm": "SHA-256",
                    "storage_type": "immutable"
                }
            }
            
            # Store in blockchain (simulated)
            self.content_registry[content_id] = blockchain_entry
            
            # Return blockchain hash
            return content_hash
            
        except Exception as e:
            return f"error_{str(e)[:20]}"
    
    async def verify_content_hash(self, content: str, content_id: str) -> Dict[str, Any]:
        """
        Verify content against stored blockchain hash
        """
        try:
            # Generate current content hash
            current_hash = self._generate_content_hash(content)
            
            # Get stored blockchain entry
            if content_id not in self.content_registry:
                return {
                    "verified": False,
                    "error": "Content not found in blockchain",
                    "current_hash": current_hash,
                    "stored_hash": None
                }
            
            stored_entry = self.content_registry[content_id]
            stored_hash = stored_entry["content_hash"]
            
            # Compare hashes
            is_verified = current_hash == stored_hash
            
            # Update verification history
            self.verification_history[content_id] = {
                "timestamp": datetime.now().isoformat(),
                "verified": is_verified,
                "current_hash": current_hash,
                "stored_hash": stored_hash
            }
            
            return {
                "verified": is_verified,
                "current_hash": current_hash,
                "stored_hash": stored_hash,
                "block_number": stored_entry["block_number"],
                "original_timestamp": stored_entry["timestamp"],
                "verification_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "verified": False,
                "error": f"Verification failed: {str(e)}",
                "current_hash": None,
                "stored_hash": None
            }
    
    async def get_content_history(self, content_id: str) -> Dict[str, Any]:
        """
        Get complete content history from blockchain
        """
        try:
            if content_id not in self.content_registry:
                return {
                    "error": "Content not found",
                    "history": []
                }
            
            stored_entry = self.content_registry[content_id]
            verification_attempts = self.verification_history.get(content_id, {})
            
            return {
                "content_id": content_id,
                "original_hash": stored_entry["content_hash"],
                "original_timestamp": stored_entry["timestamp"],
                "block_number": stored_entry["block_number"],
                "verification_attempts": verification_attempts,
                "chain_of_custody": self._build_chain_of_custody(content_id)
            }
            
        except Exception as e:
            return {
                "error": f"History retrieval failed: {str(e)}",
                "history": []
            }
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _get_next_block_number(self) -> int:
        """Get next block number (simulated)"""
        return len(self.content_registry) + 1000  # Start from 1000
    
    def _build_chain_of_custody(self, content_id: str) -> list:
        """Build chain of custody for content"""
        if content_id not in self.content_registry:
            return []
        
        chain = []
        stored_entry = self.content_registry[content_id]
        
        # Add original creation
        chain.append({
            "action": "created",
            "timestamp": stored_entry["timestamp"],
            "hash": stored_entry["content_hash"],
            "block_number": stored_entry["block_number"]
        })
        
        # Add verification attempts
        if content_id in self.verification_history:
            verification = self.verification_history[content_id]
            chain.append({
                "action": "verified" if verification["verified"] else "verification_failed",
                "timestamp": verification["timestamp"],
                "hash": verification["current_hash"],
                "match": verification["verified"]
            })
        
        return chain
    
    async def batch_verify(self, content_list: list) -> Dict[str, Any]:
        """
        Batch verify multiple content items
        """
        results = {}
        
        for content_item in content_list:
            content_id = content_item.get("content_id")
            content = content_item.get("content")
            
            if content_id and content:
                verification_result = await self.verify_content_hash(content, content_id)
                results[content_id] = verification_result
        
        return {
            "batch_results": results,
            "total_verified": sum(1 for r in results.values() if r.get("verified")),
            "total_failed": sum(1 for r in results.values() if not r.get("verified")),
            "batch_timestamp": datetime.now().isoformat()
        }

# Global instance
blockchain_verifier = BlockchainVerifier()

async def store_content_hash(content: str, content_id: str) -> str:
    """
    Main function to store content hash on blockchain
    """
    return await blockchain_verifier.store_content_hash(content, content_id)

async def verify_content_hash(content: str, content_id: str) -> Dict[str, Any]:
    """
    Main function to verify content against blockchain
    """
    return await blockchain_verifier.verify_content_hash(content, content_id)
