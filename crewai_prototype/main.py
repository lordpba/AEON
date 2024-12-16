# Warning control
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import os
import yaml
from crewai import Agent, Task, Crew

os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

# Absolute path to the YAML file
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "agents.yaml")

# Define file paths for YAML configurations
files = {
    'agents': 'crewai_prototype/agents.yaml',
    'tasks': 'crewai_prototype/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

# is possible to create a pydanit output structured, like this:
# this is an example as the agents provide as output a plan based on the
# input that they ahev received

from typing import List
from pydantic import BaseModel, Field

class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description="List of resources required to complete the task")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")

# Creating Agents
resource_manager = Agent(
  config=agents_config['resource_manager']
)

maintenance_supervisor = Agent(
  config=agents_config['maintenance_supervisor']
)

health_monitor = Agent(
  config=agents_config['health_monitor']
)

policy_manager = Agent(
    config=agents_config['policy_manager']
    )

# Creating Tasks
resource_optimization = Task(
  config=tasks_config['resource_optimization'],
  agent=resource_manager
)

maintenance_routine = Task(
  config=tasks_config['maintenance_checks'],
  agent=maintenance_supervisor
)

health_coordination = Task(
  config=tasks_config['medical_protocols'],
  agent=health_monitor,
  output_pydantic=ProjectPlan # This is the structured output we want
)

policy_decision = Task(
    config=tasks_config['policy_decision'],
    agent=policy_manager,
    output_pydantic=ProjectPlan # This is the structured output we want

)


# Creating Crew
crew = Crew(
  agents=[
    resource_manager,
    maintenance_supervisor,
    health_monitor
  ],
  tasks=[
    resource_optimization,
    maintenance_routine,
    health_coordination,
    policy_decision
  ],
  verbose=True
)

#############INPUTS################
from IPython.display import display, Markdown

project = 'Aeon'
industry = 'Aeon Technologies'
project_objectives = 'Manage resources, equipment, health, and policies for optimal performance.'
team_members = """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
"""
project_requirements = """
- Develop a comprehensive resource management system for optimal allocation
- Implement a robust equipment maintenance schedule and tracking system
- Create a health monitoring system for team members with real-time updates
- Design a policy management system for decision-making and implementation
- Ensure the system is scalable and can handle large amounts of data
- Integrate with existing Aeon Technologies infrastructure and tools
- Provide a user-friendly interface for all modules
- Ensure data security and compliance with industry standards
- Include detailed reporting and analytics capabilities
- Facilitate communication and collaboration among team members
"""

# Format the dictionary as Markdown for a better display in Jupyter Lab
formatted_output = f"""
**Project Type:** {project}

**Project Objectives:** {project_objectives}

**Industry:** {industry}

**Team Members:**
{team_members}
**Project Requirements:**
{project_requirements}
"""

# Display the formatted output as Markdown
print(formatted_output)

import pandas as pd

costs = 0.150 * (crew.usage_metrics.prompt_tokens + crew.usage_metrics.completion_tokens) / 1_000_000
print(f"Total costs: ${costs:.4f}")

# Convert UsageMetrics instance to a DataFrame
df_usage_metrics = pd.DataFrame([crew.usage_metrics.dict()])
print(df_usage_metrics)