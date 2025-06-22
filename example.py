#!/usr/bin/env python3
"""Example usage of the Social Media AI Agent models."""

from models import Agent, AgentConfig, AgentTask, AgentCapability, AgentStatus
from datetime import datetime


def main():
    """Demonstrate basic agent functionality."""
    
    print("=== Social Media AI Agent Example ===\n")
    
    # 1. Create an agent configuration
    print("1. Creating agent configuration...")
    config = AgentConfig(
        name="Social Media Content Generator",
        capabilities=[
            AgentCapability.CONTENT_GENERATION,
            AgentCapability.CONTENT_ANALYSIS,
            AgentCapability.OPTIMIZATION
        ],
        model="gpt-4",
        temperature=0.8,
        max_tokens=1500,
        system_prompt="You are an expert social media content creator."
    )
    print(f"   ✓ Created config for: {config.name}")
    print(f"   ✓ Capabilities: {[cap.value for cap in config.capabilities]}")
    print(f"   ✓ Model: {config.model}")
    print()
    
    # 2. Create an agent
    print("2. Creating agent...")
    agent = Agent(
        id="agent_001",
        config=config
    )
    print(f"   ✓ Created agent with ID: {agent.id}")
    print(f"   ✓ Status: {agent.status.value}")
    print()
    
    # 3. Create and assign a task
    print("3. Creating and assigning a task...")
    task = AgentTask(
        id="task_001",
        type="content_generation",
        parameters={
            "platform": "twitter",
            "topic": "AI and machine learning trends",
            "tone": "professional",
            "length": "280 characters"
        }
    )
    
    agent.current_task = task
    agent.status = AgentStatus.WORKING
    print(f"   ✓ Created task: {task.id}")
    print(f"   ✓ Task type: {task.type}")
    print(f"   ✓ Agent status: {agent.status.value}")
    print()
    
    # 4. Simulate task completion
    print("4. Simulating task completion...")
    task.status = AgentStatus.COMPLETED
    task.completed_at = datetime.now()
    task.result = {
        "content": "🚀 AI is revolutionizing how we work! From automated workflows to intelligent insights, machine learning is transforming industries. #AI #MachineLearning #Innovation",
        "engagement_score": 0.85,
        "hashtags": ["#AI", "#MachineLearning", "#Innovation"]
    }
    
    # Move task to history
    agent.task_history.append(task)
    agent.current_task = None
    agent.status = AgentStatus.IDLE
    
    # Update performance metrics
    agent.performance_metrics = {
        "tasks_completed": 1,
        "average_engagement": 0.85,
        "success_rate": 1.0
    }
    
    print(f"   ✓ Task completed successfully")
    print(f"   ✓ Generated content: {task.result['content']}")
    print(f"   ✓ Engagement score: {task.result['engagement_score']}")
    print(f"   ✓ Agent status: {agent.status.value}")
    print()
    
    # 5. Display agent summary
    print("5. Agent Summary:")
    print(f"   Agent ID: {agent.id}")
    print(f"   Name: {agent.config.name}")
    print(f"   Status: {agent.status.value}")
    print(f"   Tasks completed: {len(agent.task_history)}")
    print(f"   Performance metrics: {agent.performance_metrics}")
    print()
    
    print("=== Example completed successfully! ===")


if __name__ == "__main__":
    main() 