"""
AEON Colony Dashboard - Interactive Streamlit Interface
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
from datetime import datetime
import sys
from pathlib import Path

# Add code directory to path
sys.path.append(str(Path(__file__).parent))

from aeon_simulator import AEONColonySimulator
from config import ColonyConfig


# Page configuration
st.set_page_config(
    page_title="AEON Colony Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .critical-alert {
        background-color: #ff4444;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-alert {
        background-color: #ffaa00;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-alert {
        background-color: #00C851;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = None
    st.session_state.running = False
    st.session_state.last_update = time.time()


def initialize_simulator():
    """Initialize the AEON simulator"""
    if st.session_state.simulator is None:
        config = ColonyConfig(
            name=st.session_state.get('colony_name', 'AEON Alpha'),
            population_size=st.session_state.get('population', 50),
            time_scale=st.session_state.get('time_scale', 1.0)
        )
        st.session_state.simulator = AEONColonySimulator(config)
        st.session_state.simulator.start()
        st.session_state.running = True


def create_resource_gauge(resource_name: str, current: float, max_val: float, days_remaining: float):
    """Create a gauge chart for resource display"""
    percentage = (current / max_val) * 100 if max_val > 0 else 0
    
    color = "green" if percentage > 50 else "yellow" if percentage > 20 else "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        title={'text': f"{resource_name}<br><span style='font-size:0.8em'>{days_remaining:.1f} days</span>"},
        delta={'reference': max_val * 0.3},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': color},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.2
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def create_system_health_chart(systems: dict):
    """Create a bar chart for system health"""
    df = pd.DataFrame([
        {'System': info['name'], 'Health': info['health'], 'Critical': info['critical']}
        for key, info in systems.items()
    ])
    
    df['Color'] = df.apply(
        lambda row: 'red' if row['Health'] < 30 else 'orange' if row['Health'] < 70 else 'green',
        axis=1
    )
    
    fig = px.bar(
        df, 
        x='Health', 
        y='System', 
        orientation='h',
        color='Color',
        color_discrete_map={'red': '#ff4444', 'orange': '#ffaa00', 'green': '#00C851'},
        title="System Health Status"
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Health %",
        yaxis_title="",
        xaxis=dict(range=[0, 100])
    )
    
    return fig


def create_history_chart(history: list):
    """Create time series chart from history data"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Population & Morale', 'Resources', 'System Health', 'Events'),
        specs=[[{"secondary_y": True}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Population & Morale
    fig.add_trace(
        go.Scatter(x=df['sol'], y=df['population'], name='Population', line=dict(color='blue')),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=df['sol'], y=df['morale'], name='Morale', line=dict(color='green')),
        row=1, col=1, secondary_y=True
    )
    
    # Resources (stacked area)
    resources = ['water', 'food', 'energy']
    for resource in resources:
        if resource in df['resources'].iloc[0]:
            values = [r.get(resource, 0) for r in df['resources']]
            fig.add_trace(
                go.Scatter(x=df['sol'], y=values, name=resource.capitalize(), stackgroup='one'),
                row=1, col=2
            )
    
    # System Health
    fig.add_trace(
        go.Scatter(x=df['sol'], y=df['system_health'], name='System Health', 
                  fill='tozeroy', line=dict(color='purple')),
        row=2, col=1
    )
    
    # Events
    fig.add_trace(
        go.Scatter(x=df['sol'], y=df['active_events'], name='Active Events', 
                  mode='markers+lines', marker=dict(size=8, color='red')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=True, title_text="Colony Statistics History")
    
    return fig


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<p class="main-header">🚀 AEON COLONY CONTROL CENTER 🔴</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Simulation Controls")
        
        if not st.session_state.running:
            st.subheader("Colony Configuration")
            colony_name = st.text_input("Colony Name", "AEON Alpha")
            population = st.slider("Initial Population", 10, 200, 50)
            time_scale = st.slider("Time Scale", 0.1, 10.0, 1.0, 0.1)
            
            st.session_state['colony_name'] = colony_name
            st.session_state['population'] = population
            st.session_state['time_scale'] = time_scale
            
            if st.button("🚀 Start Simulation", type="primary"):
                initialize_simulator()
                st.rerun()
        else:
            sim = st.session_state.simulator
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏸️ Pause" if not sim.paused else "▶️ Resume"):
                    if sim.paused:
                        sim.resume()
                    else:
                        sim.pause()
                    st.rerun()
            
            with col2:
                if st.button("🛑 Stop"):
                    sim.stop()
                    st.session_state.running = False
                    st.session_state.simulator = None
                    st.rerun()
            
            st.markdown("---")
            
            # Time controls
            st.subheader("⏱️ Time Control")
            new_scale = st.slider("Simulation Speed", 0.1, 100.0, sim.engine.clock.time_scale, 0.1)
            if new_scale != sim.engine.clock.time_scale:
                sim.set_time_scale(new_scale)
            
            st.markdown("---")
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            if st.button("💾 Save State"):
                filename = f"saves/manual_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                sim.save_state(filename)
                st.success(f"Saved to {filename}")
            
            if st.button("🔧 Auto-Repair All"):
                current_sol = sim.engine.clock.get_current_sol()
                for system_key in sim.maintenance.systems.keys():
                    sim.maintenance.perform_maintenance(system_key, current_sol)
                st.success("All systems repaired!")
            
            if st.button("📊 Export Data"):
                st.info("Export functionality coming soon!")
    
    # Main content
    if not st.session_state.running:
        st.info("👈 Configure and start the simulation from the sidebar")
        
        # Show introductory information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🌍 About AEON")
            st.write("""
            AEON is an AI-powered autonomous governance system designed for isolated human communities,
            such as Mars colonies. It manages resources, maintains infrastructure, monitors health,
            and facilitates democratic decision-making.
            """)
        
        with col2:
            st.markdown("### 🎯 Features")
            st.write("""
            - Real-time resource management
            - Autonomous system maintenance
            - Health monitoring
            - Conflict resolution
            - Event simulation
            - Democratic governance
            """)
        
        with col3:
            st.markdown("### 🚀 Getting Started")
            st.write("""
            1. Configure your colony settings
            2. Set initial population
            3. Adjust simulation speed
            4. Click "Start Simulation"
            5. Monitor and interact!
            """)
        
        return
    
    # Get current simulator state
    sim = st.session_state.simulator
    state = sim.get_current_state()
    
    # Top status bar
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Sol (Mars Day)", f"{state['sol']:.2f}", delta=None)
        st.caption(f"Time: {state['local_time']}")
    
    with col2:
        morale_delta = state['morale'] - 75  # Compare to starting value
        st.metric("Morale", f"{state['morale']:.1f}%", f"{morale_delta:+.1f}%")
    
    with col3:
        st.metric("Population", state['population'])
    
    with col4:
        health = state['system_health']['overall_health']
        st.metric("System Health", f"{health:.1f}%", 
                 delta=None if health > 70 else "⚠️ Low" if health > 30 else "🚨 Critical")
    
    with col5:
        st.metric("Research Points", state['research_points'])
    
    st.markdown("---")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🌊 Resources", "🔧 Systems", "⚕️ Health & Society", "📜 Events & Log"
    ])
    
    with tab1:
        # Overview tab
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if sim.stats_history:
                history_chart = create_history_chart([s.to_dict() for s in sim.stats_history[-50:]])
                if history_chart:
                    st.plotly_chart(history_chart, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Colony Status")
            
            # Active alerts
            active_events = state['active_events']
            if active_events:
                st.markdown("### ⚠️ Active Events")
                for event in active_events[:5]:  # Show top 5
                    severity_color = {
                        1: "success-alert",
                        2: "warning-alert",
                        3: "warning-alert",
                        4: "critical-alert"
                    }.get(event.get('severity', 1), "warning-alert")
                    
                    st.markdown(f'<div class="{severity_color}">{event["description"]}</div>', 
                               unsafe_allow_html=True)
            else:
                st.success("✅ No active events")
            
            # Critical systems
            critical_systems = [
                sys for sys in state['system_health']['systems'].values()
                if sys['critical'] and sys['health'] < 50
            ]
            
            if critical_systems:
                st.markdown("### 🚨 Critical Systems")
                for sys in critical_systems:
                    st.error(f"{sys['name']}: {sys['health']:.1f}%")
    
    with tab2:
        # Resources tab
        st.subheader("🌊 Resource Management")
        
        resources = state['resources']
        forecast = state['resource_forecast']
        consumption = sim.config.consumption_rates
        
        cols = st.columns(len(resources))
        
        for idx, (resource, amount) in enumerate(resources.items()):
            with cols[idx]:
                daily_use = consumption.get(resource, 0) * sim.population
                days_remaining = amount / daily_use if daily_use > 0 else float('inf')
                max_capacity = sim.config.starting_resources.get(resource, amount * 2)
                
                fig = create_resource_gauge(
                    resource.capitalize(),
                    amount,
                    max_capacity,
                    days_remaining
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.caption(f"Daily use: {daily_use:.1f}")
                st.caption(f"Forecast: {forecast.get(resource, 0):.1f}")
    
    with tab3:
        # Systems tab
        st.subheader("🔧 System Maintenance")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            systems_chart = create_system_health_chart(state['system_health']['systems'])
            st.plotly_chart(systems_chart, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Maintenance Queue")
            queue = state['maintenance_queue']
            
            if queue:
                for item in queue:
                    st.write(f"**{item['name']}**")
                    st.progress(item['health'] / 100)
                    st.caption(f"Health: {item['health']:.1f}% | {'⚠️ CRITICAL' if item['critical'] else 'Normal'}")
                    
                    if st.button(f"Repair {item['name']}", key=f"repair_{item['key']}"):
                        sim.maintenance.perform_maintenance(item['key'], sim.engine.clock.get_current_sol())
                        st.success(f"Repaired {item['name']}")
                        time.sleep(0.5)
                        st.rerun()
            else:
                st.success("✅ No maintenance needed")
    
    with tab4:
        # Health & Society tab
        st.subheader("⚕️ Health & Social Cohesion")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🏥 Population Health")
            health_stats = state['health_overview']
            st.metric("Average Stress Level", f"{health_stats['average_stress']:.1f}/10")
            st.metric("Population Count", health_stats['population_count'])
            
            # Add health distribution chart here
            st.info("Detailed health metrics coming soon!")
        
        with col2:
            st.markdown("### 🤝 Social Status")
            conflicts = state['conflicts']
            st.metric("Active Conflicts", conflicts['active'])
            st.metric("Active Policies", conflicts['total_policies'])
            
            if conflicts['active'] > 0:
                st.warning(f"⚠️ {conflicts['active']} conflict(s) require attention")
            else:
                st.success("✅ Social harmony maintained")
        
        with col3:
            st.markdown("### 📋 Active Policies")
            if st.session_state.simulator:
                policies = st.session_state.simulator.policy.get_policy_overview()
                if policies:
                    # Mostra le ultime 10 policy (o tutte se meno di 10)
                    recent_policies = list(policies.items())[-10:]
                    for policy_id, description in recent_policies:
                        st.write(f"• **{policy_id}**: {description}")
                    if len(policies) > 10:
                        st.caption(f"... e altre {len(policies) - 10} policy attive")
                else:
                    st.write("Nessuna policy attiva al momento")
            else:
                st.write("Simulatore non inizializzato")
    
    with tab5:
        # Events & Log tab
        st.subheader("📜 Event Log")
        
        # Show all events
        all_events = sim.engine.events[-20:]  # Last 20 events
        
        if all_events:
            for event in reversed(all_events):
                event_dict = event.to_dict()
                
                status = "✅ Resolved" if event_dict['resolved'] else "🔴 Active"
                severity_icon = ["ℹ️", "⚠️", "‼️", "🚨"][event_dict['severity'] - 1]
                
                with st.expander(f"{severity_icon} Sol {event_dict['timestamp']:.2f}: {event_dict['description']} - {status}"):
                    st.write(f"**Type:** {event_dict['event_type']}")
                    st.write(f"**Affected Systems:** {', '.join(event_dict['affected_systems'])}")
                    st.write(f"**Consequences:** {event_dict['consequences']}")
                    
                    if not event_dict['resolved']:
                        if st.button(f"Mark as Resolved", key=f"resolve_{event_dict['timestamp']}"):
                            event.resolved = True
                            event.resolution_time = sim.engine.clock.get_current_sol()
                            st.success("Event marked as resolved")
                            st.rerun()
        else:
            st.info("No events yet")
    
    # Auto-refresh
    time.sleep(2)
    st.rerun()


if __name__ == "__main__":
    main()
