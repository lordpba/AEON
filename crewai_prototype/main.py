import os
import yaml
from crewai import Agent, Task, Crew

# Percorso assoluto al file YAML
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "agents.yaml")

# Caricare gli agenti da un file YAML
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

# Carica gli agenti
agents = load_agents_from_yaml(file_path)

# Definizione dei Task per ciascun agente
tasks = [
    Task(
        description="Analizza i dati delle risorse e ottimizza l'efficienza.",
        agent=agents[0],
        expected_output="Suggerimenti per l'allocazione delle risorse."
    ),
    Task(
        description="Monitora lo stato delle attrezzature e pianifica la manutenzione.",
        agent=agents[1],
        expected_output="Programma di manutenzione settimanale."
    ),
    Task(
        description="Analizza la salute del sistema e segnala anomalie.",
        agent=agents[2],
        expected_output="Report sulle metriche di salute e anomalie."
    ),
    Task(
        description="Analizza i report degli agenti e prende decisioni critiche.",
        agent=agents[3],
        expected_output="Override o decisioni implementabili."
    )
]

# Creazione della Crew
crew = Crew(agents=agents, tasks=tasks)

# Esecuzione della Crew
print("Avvio del sistema di governance autonoma...\n")
results = crew.kickoff()

# Output
print("\n--- RISULTATI FINALI ---")
for task, result in results.items():
    print(f"{task}: {result}")
