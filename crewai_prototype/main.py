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
# this is an example as the agents provide as aoutput a plan for a project based on the
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



# Load agents from a YAML file
def load_agents_from_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        agents = []
        for agent_data in data["agents"]:
            agent = Agent(
                name=agent_data["name"],
                role=agent_data["role"],
                goal=agent_data["goal"],
                backstory=agent_data["backstory"]
            )
            agents.append(agent)
        return agents

# Load agents
agents = load_agents_from_yaml(file_path)

# Define Tasks for each agent
tasks = [
    Task(
        description="Analyze resource data and optimize efficiency.",
        agent=agents[0],
        expected_output="Suggestions for resource allocation."
    ),
    Task(
        description="Monitor equipment status and plan maintenance.",
        agent=agents[1],
        expected_output="Weekly maintenance schedule."
    ),
    Task(
        description="Analyze people's health.",
        agent=agents[2],
        expected_output="Report on health metrics and prevention."
    ),
    Task(
        description="Analyze agents' reports and make critical decisions.",
        agent=agents[3],
        expected_output="Override or implementable decisions."
    )
]

# Create the Crew
crew = Crew(agents=agents, tasks=tasks)

# Execute the Crew
print("Starting the autonomous governance system...\n")
results = crew.kickoff()  # Ensure this returns a dictionary

# Output
print("\n--- FINAL RESULTS ---")
for task, result in results.items():
    print(f"{task}: {result}")
