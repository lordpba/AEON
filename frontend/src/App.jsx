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

// Agent XAI Log Component - Now supports real decisions
const AgentLog = ({ decisionData }) => {
  const log = decisionData || {
    decision: "Awaiting first decision request...",
    reasoning_chain: "No decision has been requested yet. Use the panel below to query AEON Core.",
    cited_wiki_pages: [],
    confidence: null
  };

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
        {log.confidence !== null && (
          <div style={{ marginBottom: '0.75rem', fontSize: '0.7rem', color: 'var(--text-tertiary)' }}>
            CONFIDENCE: <span className="json-number">{log.confidence}</span>
          </div>
        )}
        <div><span className="json-key">"decision"</span>: <span className="json-string">"{log.decision}"</span>,</div>
        <div style={{ marginTop: '0.5rem' }}><span className="json-key">"reasoning"</span>: <span className="json-string">"{log.reasoning_chain}"</span>,</div>
        {log.cited_wiki_pages?.length > 0 && (
          <div style={{ marginTop: '0.5rem' }}><span className="json-key">"sources"</span>: <span className="json-string">{JSON.stringify(log.cited_wiki_pages)}</span>,</div>
        )}
      </div>
    </div>
  );
};

// Wiki Terminal (Knowledge Base) - Supports new modular structure
const WikiTerminal = () => {
  const [pages, setPages] = useState([]);
  const [groupedPages, setGroupedPages] = useState({});
  const [activePage, setActivePage] = useState(null);
  const [content, setContent] = useState("Select a page from the LLMWiki to view Standard Operating Procedures.");
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/wiki')
      .then(res => res.json())
      .then(data => {
        if (data.pages) {
          setPages(data.pages);
          // Group pages by top-level category
          const groups = {};
          data.pages.forEach(page => {
            const parts = page.split('/');
            const category = parts.length > 1 ? parts[0] : 'other';
            
            if (!groups[category]) groups[category] = [];
            groups[category].push(page);
          });
          setGroupedPages(groups);
          setError(false);
        }
      })
      .catch(err => {
        console.error(err);
        setError(true);
        setContent("ERROR: Could not connect to AEON Backend. Is uvicorn running?");
      });
  }, []);

  const loadPage = (pagePath) => {
    setActivePage(pagePath);
    setContent("Loading...");
    // Encode the path for the URL
    const encodedPath = encodeURIComponent(pagePath);
    fetch(`http://localhost:8000/api/v1/wiki/${encodedPath}`)
      .then(res => res.json())
      .then(data => setContent(data.content))
      .catch(err => setContent("Error loading page content."));
  };

  const getCategoryLabel = (category) => {
    const labels = {
      'principles': 'Principles',
      'procedures': 'Procedures',
      'systems': 'Systems',
      'crew': 'Crew',
      'resources': 'Resources',
      'monitoring': 'Monitoring',
      'interfaces': 'Interfaces',
      'other': 'Other'
    };
    return labels[category] || category;
  };

  return (
    <div className="wiki-terminal">
      <div className="wiki-sidebar">
        <h3 className="wiki-title">LLMWiki Index</h3>
        {error ? (
          <div style={{ color: 'var(--status-critical)', fontSize: '0.875rem' }}>Backend Offline</div>
        ) : (
          <div className="wiki-groups">
            {Object.keys(groupedPages).sort().map(category => (
              <div key={category} className="wiki-group">
                <div className="wiki-group-header">{getCategoryLabel(category)}</div>
                <ul className="wiki-list">
                  {groupedPages[category].map(page => {
                    // Create a nice display name
                    const displayName = page.includes('/') 
                      ? page.split('/').slice(1).join(' / ') 
                      : page;
                    
                    return (
                      <li 
                        key={page} 
                        className={activePage === page ? 'active' : ''} 
                        onClick={() => loadPage(page)}
                        title={page}
                      >
                        📄 {displayName}
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </div>
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

  // Real decision state (Opzione B)
  const [latestDecision, setLatestDecision] = useState(null);
  const [isRequestingDecision, setIsRequestingDecision] = useState(false);
  const [decisionError, setDecisionError] = useState(null);

  // Decision request form state
  const [situation, setSituation] = useState(
    "Medical team reports a suspected pathogen. Phase 2 quarantine requires isolating several ventilation sectors, significantly increasing ECLSS power demand. The ISRU Sabatier reactors are currently operating at full capacity."
  );
  const [selectedPages, setSelectedPages] = useState([
    "principles/Emergency_Priorities",
    "procedures/contingency/Medical_Quarantine_Procedure",
    "procedures/bau/ECLSS_BAU",
    "procedures/contingency/ISRU_Sabatier_Protocol"
  ]);

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

  // Handle requesting a real decision from AEON Core
  const requestDecision = async () => {
    if (!situation.trim()) {
      setDecisionError("Please enter a situation description.");
      return;
    }

    setIsRequestingDecision(true);
    setDecisionError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/decide', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          situation: situation.trim(),
          context_pages: selectedPages
        })
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();
      const decision = data.response || data;

      setLatestDecision(decision);

    } catch (err) {
      console.error(err);
      setDecisionError("Failed to get decision. Is the backend running?");
    } finally {
      setIsRequestingDecision(false);
    }
  };

  return (
    <div className="dashboard-layout">
      
      {/* Sidebar / Agent Log */}
      <aside className="sidebar">
        <div>
          <h2 style={{ letterSpacing: '0.2em', textTransform: 'uppercase', fontSize: '1.2rem', marginBottom: '0.5rem' }}>AEON MAS</h2>
          <p style={{ color: 'var(--text-tertiary)', fontSize: '0.875rem' }}>Autonomous Extraterrestrial Operations Network</p>
        </div>
        <AgentLog decisionData={latestDecision} />
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

        {/* Decision Request Panel (Opzione B) */}
        <div className="decision-panel">
          <div className="decision-panel-header">
            <h3>Request AEON Core Decision</h3>
            <button 
              onClick={requestDecision} 
              disabled={isRequestingDecision}
              className="decision-button"
            >
              {isRequestingDecision ? "Querying AEON Core..." : "Ask AEON Core"}
            </button>
          </div>

          <div className="decision-inputs">
            <textarea
              value={situation}
              onChange={(e) => setSituation(e.target.value)}
              placeholder="Describe the situation..."
              rows={3}
            />

            <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
              Context pages used: <span className="mono" style={{ color: 'var(--accent-blue)' }}>{selectedPages.join(', ')}</span>
            </div>

            {decisionError && (
              <div style={{ color: 'var(--status-critical)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                {decisionError}
              </div>
            )}
          </div>
        </div>

        {/* Knowledge Base Viewer */}
        <WikiTerminal />
      </main>
      
    </div>
  );
}

export default App;
