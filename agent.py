#!/usr/bin/env python3
"""
NanoSutra Core – Healing Buddhi System
Receives a single JSON task → auto-evaluates risk (green/yellow/red) → executes all actions in parallel (with built-in retries) → reports back and, if clean, opens/continues a communication thread with the right audience.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any

class NanoSutraCoreAgent:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nanosutra_core.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def evaluate_risk(self, task: Dict[str, Any]) -> str:
        """
        Auto-evaluates the risk of a task.
        Returns 'green', 'yellow', or 'red'.
        
        Risk criteria:
        - Green: Standard operations, low impact, well-tested actions
        - Yellow: Medium complexity, requires validation, new audience segments
        - Red: High-risk operations, financial transactions, sensitive data
        """
        self.logger.info(f"Evaluating risk for task: {task.get('name')}")
        
        risk_score = 0
        
        # Check for high-risk keywords
        high_risk_keywords = ['delete', 'payment', 'charge', 'refund', 'cancel_subscription']
        medium_risk_keywords = ['update', 'modify', 'send_email', 'post']
        
        task_str = json.dumps(task).lower()
        
        for keyword in high_risk_keywords:
            if keyword in task_str:
                risk_score += 10
                
        for keyword in medium_risk_keywords:
            if keyword in task_str:
                risk_score += 3
        
        # Check number of actions
        num_actions = len(task.get('actions', []))MAKE AGENT TO STORE IN GIT HUB REPOSITORY THEN GO TO VERCEL
