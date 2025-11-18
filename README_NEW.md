# 🚀 AEON - GovTech Municipal Operations Platform

![AEON Banner](archive/prototypes/city_mars_prototype.jpeg)

## 🌟 Overview

**AEON** (Autonomous Environment Operations Network) è stato rifocalizzato su un POC GovTech per la gestione operativa di comunità municipali. L'engine di simulazione è day-based, l'API è esposta via FastAPI con aggiornamenti WebSocket, e un Advisor AI opzionale usa Groq (Llama).

### Key Features

- 🏙️ **Municipal Simulation** - Eventi civici, infrastruttura, servizi pubblici, governance
- 🤖 **AI Advisor (Groq)** - Raccomandazioni operative e analisi sintetiche
- 🛠️ **Infrastruttura & Servizi** - Manutenzione preventiva e allocazione risorse
- 🗳️ **Governance** - Proposte/policy con voto e quorum
- 🔔 **Eventi Dinamici** - Emergenze, allarmi ambientali, lamentele pubbliche
- 🔌 **API + WebSocket** - FastAPI + broadcast real-time per dashboard esterne

## 🎯 Project Goals

1. Create a realistic simulation of autonomous colony management
2. Research AI governance systems for isolated habitats
3. Develop a framework that's both scientifically rigorous and engaging
4. Provide a testbed for decision-making algorithms
5. Inspire future space colonization efforts

## 📦 Installazione

### Prerequisites

- Python 3.9+
- pip

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/lordpba/AEON.git
cd AEON
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Avvia il backend API**

```bash
cd backend/app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET http://localhost:8000/health`
- WebSocket live: `ws://localhost:8000/ws/simulation`
- Esempi API: `/api/v1/services/status`, `/api/v1/infrastructure/status`, `/api/v1/ai/analyze`

AI opzionale (Groq):
```bash
export GROQ_API_KEY="<la_tua_chiave>"
# opzionale: export GROQ_MODEL="llama-3.1-70b-versatile"
```

## 🎮 How to Use

### Interfaccia (frontend esterno)

1. **Collega una dashboard** (React/Vite suggerito)
   - Connetti al WebSocket per aggiornamenti (`/ws/simulation`)
   - Chiama le API per azioni (es. manutenzione, proposte)

2. **Monitor Status**
   - **Overview Tab**: General statistics and trends
   - **Resources Tab**: Water, food, energy levels with forecasting
   - **Systems Tab**: Infrastructure health and maintenance queue
   - **Health & Society Tab**: Population wellbeing and conflicts
   - **Events & Log Tab**: History of events and crises

3. **Interagisci**
   - Pianifica manutenzioni, alloca servizi
   - Crea/vota proposte di governance
   - Richiedi analisi all'AI Advisor

### Esempio programmatico (Python)

```python
from municipal_simulator import AEONMunicipalSimulator
from config import CommunityConfig

sim = AEONMunicipalSimulator(CommunityConfig(name="Small Town"))
sim.start()
print(sim.get_detailed_status()["time"])  # stato rapido
sim.stop()
```

## 🏗️ Project Structure

```
AEON/
├── code/
│   ├── municipal_simulator.py  # Municipal simulator orchestrator
│   ├── config.py               # Configuration management
│   ├── simulation_engine.py    # Time and event management
│   └── modules/
│       ├── resources.py        # Resource management
│       ├── maintenance.py      # System maintenance
│       ├── health.py           # Health monitoring
│       ├── policy.py           # Governance and conflicts
│       └── human.py            # Human supervision
├── backend/                    # FastAPI backend (API + WebSocket)
├── saves/                      # Saved simulation states
├── logs/                       # Simulation logs
└── requirements.txt            # Python dependencies
```

## 🧪 Research Applications

AEON can be used for:

1. **AI Decision-Making Research**
   - Test autonomous governance algorithms
   - Study resource optimization strategies
   - Evaluate crisis response systems

2. **Human Factors Studies**
   - Simulate psychological stress in isolation
   - Model social dynamics in confined spaces
   - Test conflict resolution mechanisms

3. **System Resilience Testing**
   - Evaluate redundancy requirements
   - Test failure cascade scenarios
   - Optimize maintenance schedules

4. **Educational Tool**
   - Teach systems thinking
   - Demonstrate complexity theory
   - Inspire STEM education

## 🎲 Game Mode Features

Play AEON as a colony management game:

- **Survival Mode**: Keep your colony alive as long as possible
- **Expansion Mode**: Grow from 10 to 1000 colonists
- **Crisis Mode**: Handle extreme scenarios
- **Research Goals**: Unlock technologies and discoveries
- **Achievements**: Complete challenging objectives

## 🔮 Roadmap

### Phase 1: Core Systems ✅ (COMPLETED)
- [x] Resource management
- [x] System maintenance
- [x] Event system
- [x] Time-based simulation
- [x] Interactive dashboard

### Phase 2: AI Integration 🚧 (IN PROGRESS)
- [x] Integrazione Groq (endpoint base)
- [ ] Prompt avanzati e azioni consigliate
- [ ] Analisi budget/emergenze/sentiment

### Phase 3: Advanced Features 📋 (PLANNED)
- [ ] DAO integration for democratic governance
- [ ] Multi-colony management
- [ ] Trade between colonies
- [ ] Technology research tree
- [ ] Procedural event generation

### Phase 4: Polish & Release 🎯 (FUTURE)
- [ ] Tutorial system
- [ ] Campaign scenarios
- [ ] Mod support
- [ ] Mobile interface
- [ ] Multiplayer collaboration

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **AI/ML**: Improve decision-making algorithms
- **Game Design**: Balance mechanics and add features
- **UI/UX**: Enhance the dashboard
- **Research**: Validate against real Mars mission data
- **Documentation**: Improve guides and examples

## 📚 Scientific Background

AEON is based on research in:

- Autonomous systems and robotics
- Life support systems for space habitats
- Closed-loop ecological systems
- AI governance and ethics
- Human factors in extreme environments
- Systems engineering and reliability

### References

- NASA Mars Design Reference Architecture
- ESA Moon Village concepts
- Research on ICE habitats (International Space Station, Antarctic bases)
- AI governance frameworks (OpenAI, DeepMind)

## 📝 License

[Add your license here - MIT, Apache, GPL, etc.]

## 👥 Team

- **Creator**: lordpba
- **Inspired by**: AEON Chronicles (sci-fi novel)
- **Contributors**: [Your contributors]

## 🌐 Links

- [AEON Chronicles Novel](https://medium.com/@mario.pba/aeon-chronicles-e37ae94d9a45)
- [Documentation](./docs/)
- [GitHub Issues](https://github.com/lordpba/AEON/issues)

## 🙏 Acknowledgments

- Inspired by games like Surviving Mars, Rimworld, Oxygen Not Included
- Built with Python, FastAPI, and Groq (opzionale)
- Mars data from NASA and ESA missions

---

**"The future of humanity among the stars begins with intelligent systems that can sustain life in the harshest environments."**

🚀 Start your colony today!
