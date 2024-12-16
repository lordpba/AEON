import os
import yaml
from crewai import Agent, Task, Crew

# Absolute path to the YAML file
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "agents.yaml")

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
