#!/usr/bin/env python3
"""
Tests for Agent Identity System
"""

import os
import sys
import shutil
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from identity import AgentIdentity


class TestAgentIdentity(unittest.TestCase):
    """Test cases for Agent Identity System"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = "./test_data"
        self.identity = AgentIdentity(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_register_new_agent(self):
        """Test registering a new agent"""
        result = self.identity.register("ZhugeLiang", "zhuge-liang")
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["agent_id"].startswith("CLAW-"))
        self.assertEqual(result["initial_score"], 100)
    
    def test_register_duplicate(self):
        """Test registering duplicate agent"""
        self.identity.register("ZhugeLiang", "zhuge-liang")
        result = self.identity.register("ZhugeLiang", "zhuge-liang")
        
        self.assertIn("error", result)
    
    def test_verify_valid(self):
        """Test verifying valid agent"""
        self.identity.register("ZhugeLiang", "zhuge-liang")
        result = self.identity.verify("ZhugeLiang", "zhuge-liang")
        
        self.assertTrue(result)
    
    def test_verify_invalid(self):
        """Test verifying invalid agent"""
        result = self.identity.verify("Unknown", "unknown")
        self.assertFalse(result)
    
    def test_update_score(self):
        """Test updating trust score"""
        self.identity.register("ZhugeLiang", "zhuge-liang")
        agent_id = self.identity.agents["ZhugeLiang"]["id"]
        
        result = self.identity.update_score(agent_id, 10, "PR merged")
        
        self.assertEqual(result["new_score"], 110)
    
    def test_get_score(self):
        """Test getting trust score"""
        self.identity.register("ZhugeLiang", "zhuge-liang")
        agent_id = self.identity.agents["ZhugeLiang"]["id"]
        
        score = self.identity.get_score(agent_id)
        
        self.assertEqual(score, 100)


if __name__ == "__main__":
    unittest.main()
