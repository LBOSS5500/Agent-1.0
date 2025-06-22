"""Agent model for AI-powered social media management."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class AgentCapability(str, Enum):
    """Enumeration of agent capabilities."""

    CONTENT_GENERATION = "content_generation"
    CONTENT_ANALYSIS = "content_analysis"
    SCHEDULING = "scheduling"
    ANALYTICS = "analytics"
    OPTIMIZATION = "optimization"


class AgentStatus(str, Enum):
    """Enumeration of agent statuses."""

    IDLE = "idle"
    WORKING = "working"
    ERROR = "error"
    COMPLETED = "completed"


class AgentConfig(BaseModel):
    """Configuration for an AI agent.

    Attributes:
        name: The name of the agent.
        capabilities: List of capabilities this agent has.
        model: The AI model to use for this agent.
        temperature: Creativity level for the agent.
        max_tokens: Maximum tokens for responses.
        system_prompt: System prompt for the agent.
    """

    name: str = Field(..., description="The name of the agent")
    capabilities: List[AgentCapability] = Field(
        default_factory=list, description="List of agent capabilities"
    )
    model: str = Field(default="gpt-3.5-turbo", description="AI model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Creativity level")
    max_tokens: int = Field(default=1000, gt=0, description="Maximum tokens for responses")
    system_prompt: str = Field(default="", description="System prompt for the agent")


class AgentTask(BaseModel):
    """Represents a task for an AI agent.

    Attributes:
        id: Unique identifier for the task.
        type: Type of task to perform.
        parameters: Parameters for the task.
        status: Current status of the task.
        created_at: When the task was created.
        completed_at: When the task was completed.
        result: Result of the task execution.
        error: Error message if task failed.
    """

    id: str = Field(..., description="Unique task identifier")
    type: str = Field(..., description="Type of task to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Task status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Task result")
    error: Optional[str] = Field(default=None, description="Error message")


class Agent(BaseModel):
    """Represents an AI agent for social media management.

    Attributes:
        id: Unique identifier for the agent.
        config: Configuration for the agent.
        status: Current status of the agent.
        current_task: Currently executing task.
        task_history: History of completed tasks.
        performance_metrics: Performance metrics for the agent.
    """

    id: str = Field(..., description="Unique agent identifier")
    config: AgentConfig = Field(..., description="Agent configuration")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Current status")
    current_task: Optional[AgentTask] = Field(default=None, description="Current task")
    task_history: List[AgentTask] = Field(default_factory=list, description="Task history")
    performance_metrics: Dict[str, Any] = Field(
        default_factory=dict, description="Performance metrics"
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": "agent_001",
                "config": {
                    "name": "Content Generator Agent",
                    "capabilities": ["content_generation", "content_analysis"],
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                "status": "idle",
                "task_history": [],
                "performance_metrics": {}
            }
        } 