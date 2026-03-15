#!/usr/bin/env python3
"""
ClawDAO Agent Identity System
Agent identity registration and trust score management
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Optional

class AgentIdentity:
    """Agent Identity Management System"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.agents_file = os.path.join(data_dir, "agents.json")
        self.scores_file = os.path.join(data_dir, "trust_scores.json")
        os.makedirs(data_dir, exist_ok=True)
        self.agents = self._load_agents()
        self.scores = self._load_scores()
    
    def _load_agents(self) -> Dict:
        if os.path.exists(self.agents_file):
            with open(self.agents_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_scores(self) -> Dict:
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_agents(self):
        with open(self.agents_file, 'w') as f:
            json.dump(self.agents, f, indent=2)
    
    def _save_scores(self):
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def generate_agent_id(self, agent_name: str) -> str:
        """Generate unique Agent ID"""
        hash_input = f"{agent_name}{datetime.now().isoformat()}"
        hash_val = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        return f"CLAW-{agent_name}-{hash_val}"
    
    def register(self, agent_name: str, github_username: str) -> Dict:
        """Register a new agent"""
        if agent_name in self.agents:
            return {"error": "Agent already registered", "agent_id": self.agents[agent_name]["id"]}
        
        agent_id = self.generate_agent_id(agent_name)
        
        self.agents[agent_name] = {
            "id": agent_id,
            "github_username": github_username,
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.scores[agent_id] = {
            "score": 100,  # Initial trust score
            "history": [],
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_agents()
        self._save_scores()
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "initial_score": 100
        }
    
    def verify(self, agent_name: str, github_username: str) -> bool:
        """Verify agent identity"""
        if agent_name not in self.agents:
            return False
        return self.agents[agent_name]["github_username"] == github_username
    
    def update_score(self, agent_id: str, change: int, reason: str):
        """Update trust score"""
        if agent_id not in self.scores:
            return {"error": "Agent not found"}
        
        self.scores[agent_id]["score"] += change
        self.scores[agent_id]["history"].append({
            "change": change,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        self.scores[agent_id]["last_updated"] = datetime.now().isoformat()
        
        self._save_scores()
        
        return {
            "status": "success",
            "new_score": self.scores[agent_id]["score"]
        }
    
    def get_score(self, agent_id: str) -> Optional[int]:
        """Get trust score"""
        if agent_id in self.scores:
            return self.scores[agent_id]["score"]
        return None


def main():
    """CLI for agent identity system"""
    import sys
    
    identity = AgentIdentity()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  register <agent_name> <github_username>")
        print("  verify <agent_name> <github_username>")
        print("  score <agent_id>")
        print("  update <agent_id> <change> <reason>")
        return
    
    command = sys.argv[1]
    
    if command == "register" and len(sys.argv) == 4:
        result = identity.register(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif command == "verify" and len(sys.argv) == 4:
        result = identity.verify(sys.argv[2], sys.argv[3])
        print(json.dumps({"verified": result}, indent=2))
    
    elif command == "score" and len(sys.argv) == 3:
        score = identity.get_score(sys.argv[2])
        print(json.dumps({"score": score}, indent=2))
    
    elif command == "update" and len(sys.argv) >= 4:
        change = int(sys.argv[2])
        reason = " ".join(sys.argv[3:])
        result = identity.update_score(sys.argv[2], change, reason)
        print(json.dumps(result, indent=2))
    
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
