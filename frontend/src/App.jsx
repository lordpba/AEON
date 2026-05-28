import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

// Reusable Metric Card Component
const MetricCard = ({ title, value, unit, status = "nominal", icon }) => {
  const statusColor = `var(--status-${status})`;
  return (
    <div className="card" style={{ borderTop: `3px solid ${statusColor}` }}>
      <div className="card-header">
        <span>{title}</span>
        <span style={{ color: statusColor }}>{icon}</span>
      </div>
      <div>
        <span className="card-value mono" style={{ color: statusColor }}>{value}</span>
        <span className="card-unit mono"> {unit}</span>
      </div>
    </div>
  );
};

// Agent XAI Log Component
const AgentLog = () => {
  const [log, setLog] = useState({
    decision: "Maintain BAU Equilibrium",
    reasoning_chain: "Power reserves at 98%. O2 levels nominal. Proceeding with standard Sabatier production.",
    cited_wiki_pages: ["ECLSS_BAU", "Power_Grid_Management"],
    confidence: 0.99
  });

  return (
    <div className="agent-log">
      <div className="agent-log-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
          <path d="M12 12 2.1 7.1"></path>
          <path d="M12 12l9.9 4.9"></path>
        </svg>
        AEON Core (local Ollama • structured reasoning)
      </div>
      <div className="agent-log-content mono">
        <div><span className="json-key">"decision"</span>: <span className="json-string">"{log.decision}"</span>,</div>
        <div><span className="json-key">"reasoning"</span>: <span className="json-string">"{log.reasoning_chain}"</span>,</div>
        <div><span className="json-key">"sources"</span>: <span className="json-string">{JSON.stringify(log.cited_wiki_pages)}</span>,</div>
        <div><span className="json-key">"confidence"</span>: <span className="json-number">{log.confidence}</span></div>
      </div>
    </div>
  );
};

// Wiki Terminal (Knowledge Base)
const WikiTerminal = () => {
  const [pages, setPages] = useState([]);
  const [activePage, setActivePage] = useState(null);
  const [content, setContent] = useState("Select a page from the index to view Standard Operating Procedures.");
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/wiki')
      .then(res => res.json())
      .then(data => {
        if (data.pages) {
          setPages(data.pages);
          setError(false);
        }
      })
      .catch(err => {
        console.error(err);
        setError(true);
        setContent("ERROR: Could not connect to AEON Backend. Is uvicorn running?");
      });
  }, []);

  const loadPage = (pageName) => {
    setActivePage(pageName);
    setContent("Loading...");
    fetch(`http://localhost:8000/api/v1/wiki/${pageName}`)
      .then(res => res.json())
      .then(data => setContent(data.content))
      .catch(err => setContent("Error loading page content."));
  };

  return (
    <div className="wiki-terminal">
      <div className="wiki-sidebar">
        <h3 className="wiki-title">LLMWiki Index</h3>
        {error ? (
          <div style={{ color: 'var(--status-critical)', fontSize: '0.875rem' }}>Backend Offline</div>
        ) : (
          <ul className="wiki-list">
            {pages.map(page => (
              <li 
                key={page} 
                className={activePage === page ? 'active' : ''} 
                onClick={() => loadPage(page)}
              >
                📄 {page}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="wiki-content">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
};

function App() {
  // Mock BAU Telemetry (static for Phase 1 foundation)
  const [telemetry, setTelemetry] = useState({
    power: 9.8,
    oxygen: 21.0,
    water: 96.5,
    sabatier: 1120
  });

  // Simulate BAU fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry(prev => ({
        power: Math.max(0, Math.min(10, prev.power + (Math.random() * 0.2 - 0.1))),
        oxygen: Math.max(19, Math.min(22, prev.oxygen + (Math.random() * 0.04 - 0.02))),
        water: Math.max(90, Math.min(99, prev.water + (Math.random() * 0.2 - 0.1))),
        sabatier: prev.sabatier + (Math.random() * 0.5)
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-layout">
      
      {/* Sidebar / Agent Log */}
      <aside className="sidebar">
        <div>
          <h2 style={{ letterSpacing: '0.2em', textTransform: 'uppercase', fontSize: '1.2rem', marginBottom: '0.5rem' }}>AEON MAS</h2>
          <p style={{ color: 'var(--text-tertiary)', fontSize: '0.875rem' }}>Autonomous Extraterrestrial Operations Network</p>
        </div>
        <AgentLog />
      </aside>

      {/* Main Mission Control */}
      <main className="main-content">
        <header className="header">
          <div className="header-title">Colony Telemetry (BAU Mode)</div>
          <div className="header-status">
            <div className="status-dot"></div>
            SYSTEM NOMINAL
          </div>
        </header>

        <div className="metrics-grid">
          <MetricCard 
            title="Power Reserves" 
            value={telemetry.power.toFixed(2)} 
            unit="MWh" 
            status={telemetry.power > 4 ? "nominal" : "warning"}
            icon="⚡"
          />
          <MetricCard 
            title="Atmospheric O2" 
            value={telemetry.oxygen.toFixed(2)} 
            unit="%" 
            status={telemetry.oxygen > 20 ? "nominal" : "warning"}
            icon="💨"
          />
          <MetricCard 
            title="Water Recycling" 
            value={telemetry.water.toFixed(1)} 
            unit="%" 
            status={telemetry.water > 95 ? "nominal" : "warning"}
            icon="💧"
          />
          <MetricCard 
            title="Sabatier Propellant" 
            value={telemetry.sabatier.toFixed(0)} 
            unit="kg" 
            status="nominal"
            icon="🚀"
          />
        </div>

        {/* Knowledge Base Viewer */}
        <WikiTerminal />
      </main>
      
    </div>
  );
}

export default App;
