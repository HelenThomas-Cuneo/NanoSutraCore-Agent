       #!/usr/bin/env python3
“””
NanoSutra Core - Healing Buddhi System
Receives a single JSON task → auto-evaluates risk (green/yellow/red) → executes all actions in parallel
“””

import asyncio
import json
import logging
from typing import Dict, List, Any
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

class NanoSutraCoreAgent:
def **init**(self):
self.setup_logging()

```
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

async def evaluate_risk(self, task: Dict[str, Any]) -> str:
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
    num_actions = len(task.get('actions', []))
    if num_actions > 5:
        risk_score += 5
    elif num_actions > 3:
        risk_score += 2
    
    # Determine risk level based on score
    if risk_score >= 10:
        return 'red'
    elif risk_score >= 5:
        return 'yellow'
    else:
        return 'green'

async def execute_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Executes all actions in parallel.
    Returns a list of results for each action.
    """
    self.logger.info(f"Executing {len(actions)} actions in parallel")
    
    async def execute_single_action(action: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate action execution
        await asyncio.sleep(0.1)  # Simulate some processing time
        return {
            'action': action.get('type', 'unknown'),
            'status': 'success',
            'result': f"Executed {action.get('type', 'unknown')} action"
        }
    
    # Execute all actions concurrently
    results = await asyncio.gather(
        *[execute_single_action(action) for action in actions]
    )
    
    return results

async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main processing function that evaluates risk and executes actions.
    """
    self.logger.info(f"Processing task: {task.get('name', 'Unnamed Task')}")
    
    # Evaluate risk
    risk_level = await self.evaluate_risk(task)
    self.logger.info(f"Risk level determined: {risk_level}")
    
    # Execute actions
    actions = task.get('actions', [])
    results = await self.execute_actions(actions)
    
    return {
        'task_name': task.get('name', 'Unnamed Task'),
        'risk_level': risk_level,
        'actions_executed': len(actions),
        'results': results,
        'status': 'completed'
    }
```

# Create Flask app

app = Flask(**name**)
CORS(app)  # Enable CORS so your frontend can talk to this API

# Initialize the agent

agent = NanoSutraCoreAgent()

@app.route(’/’)
def home():
“”“Serve the main HTML page”””
return send_file(‘index.html’)

@app.route(’/api/health’, methods=[‘GET’])
def health_check():
“”“Health check endpoint to verify the API is running”””
return jsonify({
‘status’: ‘healthy’,
‘message’: ‘NanoSutra Core Agent is running’
})

@app.route(’/api/evaluate’, methods=[‘POST’])
def evaluate_task():
“””
Main endpoint for task evaluation.
Receives a task JSON, evaluates risk, and executes actions.
“””
try:
task_data = request.json

```
    if not task_data:
        return jsonify({
            'error': 'No task data provided'
        }), 400
    
    # Process the task asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(agent.process_task(task_data))
    loop.close()
    
    return jsonify(result)

except Exception as e:
    app.logger.error(f"Error processing task: {str(e)}")
    return jsonify({
        'error': str(e),
        'status': 'failed'
    }), 500
```

@app.route(’/api/test/<risk_type>’, methods=[‘GET’])
def test_task(risk_type):
“””
Test endpoint that creates sample tasks for different risk levels.
risk_type can be: ‘supervision’, ‘standard’, ‘green’, or ‘red’
“””
test_tasks = {
‘supervision’: {
‘name’: ‘Supervision Task - High Oversight Required’,
‘description’: ‘Critical operation requiring human approval’,
‘actions’: [
{‘type’: ‘verify_identity’, ‘data’: ‘user_123’},
{‘type’: ‘check_permissions’, ‘data’: ‘admin_level’},
{‘type’: ‘log_action’, ‘data’: ‘supervision_check’}
]
},
‘standard’: {
‘name’: ‘Standard Task - Normal Operations’,
‘description’: ‘Regular task with moderate complexity’,
‘actions’: [
{‘type’: ‘fetch_data’, ‘data’: ‘records’},
{‘type’: ‘update’, ‘data’: ‘status_field’},
{‘type’: ‘notify’, ‘data’: ‘team_channel’}
]
},
‘green’: {
‘name’: ‘Green Risk Task - Safe Operations’,
‘description’: ‘Low-risk task with well-tested actions’,
‘actions’: [
{‘type’: ‘read_data’, ‘data’: ‘user_profile’},
{‘type’: ‘log’, ‘data’: ‘access_time’}
]
},
‘red’: {
‘name’: ‘Red Risk Task - High-Risk Operations’,
‘description’: ‘Dangerous task requiring extreme caution’,
‘actions’: [
{‘type’: ‘delete’, ‘data’: ‘user_account’},
{‘type’: ‘charge’, ‘data’: ‘payment_$500’},
{‘type’: ‘refund’, ‘data’: ‘transaction_xyz’},
{‘type’: ‘cancel_subscription’, ‘data’: ‘premium_plan’}
]
}
}

```
task = test_tasks.get(risk_type)
if not task:
    return jsonify({
        'error': f'Unknown risk type: {risk_type}'
    }), 400

# Process the test task
try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(agent.process_task(task))
    loop.close()
    
    return jsonify(result)

except Exception as e:
    app.logger.error(f"Error processing test task: {str(e)}")
    return jsonify({
        'error': str(e),
        'status': 'failed'
    }), 500
```

# This is critical for Vercel - it needs to find the ‘app’ object

if **name** == ‘**main**’:
# This runs when you test locally, but Vercel will use the ‘app’ object directly
app.run(debug=True, host=‘0.0.0.0’, port=5000)
