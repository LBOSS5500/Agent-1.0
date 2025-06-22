#!/usr/bin/env python3
"""Flask web application for Agent-1.0."""

from flask import Flask, request, jsonify
from models import Agent, AgentConfig, AgentTask, AgentCapability, AgentStatus
from datetime import datetime
import uuid
import os

app = Flask(__name__)

# In-memory storage for demo purposes
agents = {}

@app.route('/')
def home():
    """Home page with basic information."""
    return jsonify({
        "message": "Agent-1.0 API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This information",
            "POST /agents": "Create a new agent",
            "GET /agents": "List all agents",
            "GET /agents/<id>": "Get agent details",
            "POST /agents/<id>/tasks": "Create a task for an agent",
            "GET /agents/<id>/tasks": "Get agent tasks"
        }
    })

@app.route('/agents', methods=['POST'])
def create_agent():
    """Create a new agent."""
    try:
        data = request.get_json()
        
        config = AgentConfig(
            name=data.get('name', 'Default Agent'),
            capabilities=data.get('capabilities', [AgentCapability.CONTENT_GENERATION]),
            model=data.get('model', 'gpt-3.5-turbo'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 1000),
            system_prompt=data.get('system_prompt', '')
        )
        
        agent_id = str(uuid.uuid4())
        agent = Agent(
            id=agent_id,
            config=config
        )
        
        agents[agent_id] = agent
        
        return jsonify({
            "message": "Agent created successfully",
            "agent": {
                "id": agent.id,
                "name": agent.config.name,
                "capabilities": [cap.value for cap in agent.config.capabilities],
                "status": agent.status.value
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/agents', methods=['GET'])
def list_agents():
    """List all agents."""
    return jsonify({
        "agents": [
            {
                "id": agent.id,
                "name": agent.config.name,
                "capabilities": [cap.value for cap in agent.config.capabilities],
                "status": agent.status.value,
                "tasks_completed": len(agent.task_history)
            }
            for agent in agents.values()
        ]
    })

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get agent details."""
    if agent_id not in agents:
        return jsonify({"error": "Agent not found"}), 404
    
    agent = agents[agent_id]
    return jsonify({
        "id": agent.id,
        "config": {
            "name": agent.config.name,
            "capabilities": [cap.value for cap in agent.config.capabilities],
            "model": agent.config.model,
            "temperature": agent.config.temperature,
            "max_tokens": agent.config.max_tokens
        },
        "status": agent.status.value,
        "current_task": agent.current_task.dict() if agent.current_task else None,
        "task_history": [task.dict() for task in agent.task_history],
        "performance_metrics": agent.performance_metrics
    })

@app.route('/agents/<agent_id>/tasks', methods=['POST'])
def create_task(agent_id):
    """Create a task for an agent."""
    if agent_id not in agents:
        return jsonify({"error": "Agent not found"}), 404
    
    try:
        data = request.get_json()
        
        task = AgentTask(
            id=str(uuid.uuid4()),
            type=data.get('type', 'content_generation'),
            parameters=data.get('parameters', {})
        )
        
        agent = agents[agent_id]
        agent.current_task = task
        agent.status = AgentStatus.WORKING
        
        return jsonify({
            "message": "Task created successfully",
            "task": {
                "id": task.id,
                "type": task.type,
                "status": task.status.value,
                "created_at": task.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/agents/<agent_id>/tasks', methods=['GET'])
def get_agent_tasks(agent_id):
    """Get agent tasks."""
    if agent_id not in agents:
        return jsonify({"error": "Agent not found"}), 404
    
    agent = agents[agent_id]
    return jsonify({
        "current_task": agent.current_task.dict() if agent.current_task else None,
        "task_history": [task.dict() for task in agent.task_history]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False) 