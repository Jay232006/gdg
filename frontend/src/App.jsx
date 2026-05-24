import React, { useState, useEffect, useRef } from 'react';

// Custom lightweight markdown renderer to display rich formatting in chat bubbles
const parseBold = (str) => {
  const parts = str.split('**');
  return parts.map((part, i) => i % 2 === 1 ? <strong key={i}>{part}</strong> : part);
};

const formatMarkdown = (text) => {
  if (!text) return '';
  const lines = text.split('\n');
  return lines.map((line, idx) => {
    const trimmed = line.trim();
    if (trimmed.startsWith('### ')) {
      return <h3 key={idx} style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '1.2rem', color: '#00d2ff' }}>{trimmed.substring(4)}</h3>;
    }
    if (trimmed.startsWith('#### ')) {
      return <h4 key={idx} style={{ marginTop: '0.75rem', marginBottom: '0.25rem', fontSize: '1rem', color: '#e2e8f0' }}>{trimmed.substring(5)}</h4>;
    }
    if (trimmed.startsWith('> ')) {
      return <blockquote key={idx} style={{ borderLeft: '3px solid #00d2ff', paddingLeft: '0.75rem', margin: '0.75rem 0', fontStyle: 'italic', background: 'rgba(255,255,255,0.03)', padding: '0.5rem' }}>{parseBold(trimmed.substring(2))}</blockquote>;
    }
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      return <li key={idx} style={{ marginLeft: '1.25rem', listStyleType: 'disc', fontSize: '0.9rem' }}>{parseBold(trimmed.substring(2))}</li>;
    }
    if (/^\d+\.\s/.test(trimmed)) {
      const cleanText = trimmed.replace(/^\d+\.\s/, '');
      return <li key={idx} style={{ marginLeft: '1.25rem', listStyleType: 'decimal', fontSize: '0.9rem' }}>{parseBold(cleanText)}</li>;
    }
    if (!trimmed) {
      return <div key={idx} style={{ height: '0.5rem' }}></div>;
    }
    return <p key={idx} style={{ marginBottom: '0.4rem', fontSize: '0.9rem' }}>{parseBold(line)}</p>;
  });
};

function App() {
  // Tab states: 'overview', 'nutrition', 'rehab', 'chat'
  const [activeTab, setActiveTab] = useState('overview');

  // Player state
  const [profile, setProfile] = useState({
    name: 'Jasprit Singh',
    role: 'Fast Bowler',
    weight: 80.0,
    height: 183.0,
    age: 27,
    format_type: 'Test',
    active_injury: 'None'
  });
  const [profileSaved, setProfileSaved] = useState(false);

  // Wellness and Workload state
  const [wellnessLogs, setWellnessLogs] = useState([]);
  const [acwr, setAcwr] = useState({
    acute_workload: 0,
    chronic_workload: 0,
    acwr: 0,
    zone: 'Unknown',
    risk_description: 'Loading...',
    color_code: '#94a3b8',
    status_key: 'under'
  });

  // Daily Check-in Form state
  const [wellnessForm, setWellnessForm] = useState({
    sleep_hours: 8,
    soreness_level: 2,
    fatigue_level: 2,
    training_hours: 2,
    rpe: 5
  });
  const [wellnessLoggedToday, setWellnessLoggedToday] = useState(false);

  // Chat states
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatBottomRef = useRef(null);

  // Injury Rehab details state
  const [rehabGuide, setRehabGuide] = useState(null);
  const [checkedExercises, setCheckedExercises] = useState({});

  // API connection check
  const [apiError, setApiError] = useState(null);

  // Fetch initial profile, wellness logs, and chat history
  useEffect(() => {
    fetchProfile();
    fetchWellness();
    fetchChatHistory();
  }, []);

  // Fetch rehab guide when active injury changes
  useEffect(() => {
    if (profile.active_injury && profile.active_injury !== 'None') {
      fetchRehabGuide(profile.active_injury);
    } else {
      setRehabGuide(null);
    }
  }, [profile.active_injury]);

  // Scroll to bottom of chat
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, chatLoading]);

  const fetchProfile = async () => {
    try {
      const res = await fetch('/api/profile');
      if (!res.ok) throw new Error("Failed to load profile");
      const data = await res.json();
      setProfile(data);
      setApiError(null);
    } catch (err) {
      console.error(err);
      setApiError("Cannot connect to the backend server. Please verify the backend is running on http://localhost:8000.");
    }
  };

  const saveProfile = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      });
      if (!res.ok) throw new Error("Failed to save profile");
      const data = await res.json();
      setProfile(data);
      setProfileSaved(true);
      setTimeout(() => setProfileSaved(false), 3000);
      fetchWellness(); // Profile change can update macro outputs or active logs
    } catch (err) {
      console.error(err);
    }
  };

  const fetchWellness = async () => {
    try {
      const res = await fetch('/api/wellness');
      if (!res.ok) throw new Error("Failed to load wellness logs");
      const data = await res.json();
      setWellnessLogs(data.logs || []);
      setAcwr(data.acwr || {});
      
      // Check if logged today
      const todayStr = new Date().toISOString().split('T')[0];
      const loggedToday = data.logs.some(log => log.date === todayStr);
      setWellnessLoggedToday(loggedToday);
    } catch (err) {
      console.error(err);
    }
  };

  const logDailyWellness = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/wellness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wellnessForm)
      });
      if (!res.ok) throw new Error("Failed to log wellness");
      await res.json();
      setWellnessLoggedToday(true);
      fetchWellness();
      
      // Add a system announcement to the chat regarding updated workload
      fetchChatHistory();
    } catch (err) {
      console.error(err);
    }
  };

  const fetchChatHistory = async () => {
    try {
      const res = await fetch('/api/chat/history');
      if (!res.ok) throw new Error("Failed to load chat history");
      const data = await res.json();
      setMessages(data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const sendChatMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userText = chatInput;
    setChatInput('');
    
    // Add user message locally first for responsive feel
    const tempUserMsg = { id: Date.now(), sender: 'user', message: userText, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, tempUserMsg]);
    setChatLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText })
      });
      if (!res.ok) throw new Error("Failed to get agent response");
      const data = await res.json();
      
      // Refresh chat logs from DB to get the verified stored entries
      fetchChatHistory();
      fetchWellness(); // In case the chat response contains workload changes
    } catch (err) {
      console.error(err);
      // Fallback display if error
      const tempCoachMsg = { id: Date.now() + 1, sender: 'coach', message: "Error communicating with AI Coach. Please make sure the backend is active.", timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, tempCoachMsg]);
    } finally {
      setChatLoading(false);
    }
  };

  const fetchRehabGuide = async (injuryKey) => {
    try {
      const res = await fetch(`/api/rehab/${injuryKey}`);
      if (!res.ok) throw new Error("Failed to load rehab guide");
      const data = await res.json();
      setRehabGuide(data);
    } catch (err) {
      console.error(err);
      setRehabGuide(null);
    }
  };

  const toggleExercise = (name) => {
    setCheckedExercises(prev => ({
      ...prev,
      [name]: !prev[name]
    }));
  };

  const resetAllData = async () => {
    if (!window.confirm("Are you sure you want to clear chat and training logs? This will seed a clean history.")) return;
    try {
      const res = await fetch('/api/reset', { method: 'POST' });
      if (!res.ok) throw new Error("Reset failed");
      fetchProfile();
      fetchWellness();
      fetchChatHistory();
      setCheckedExercises({});
    } catch (err) {
      console.error(err);
    }
  };

  // Pre-calculate nutrition numbers locally for UI display
  const calculateMacros = () => {
    const { weight, height, age, role, format_type } = profile;
    const training_hours = wellnessForm.training_hours || 2;
    
    const bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
    let tdee = bmr * (1.2 + 0.15 * training_hours);
    
    // role adjustments
    const roleAdjust = { 'Fast Bowler': 450, 'All-rounder': 300, 'Wicketkeeper': 250, 'Batter': 150, 'Spinner': 150 };
    tdee += roleAdjust[role] || 150;
    
    // format adjustments
    const formatAdjust = { 'Test': 600, 'ODI': 400, 'T20': 200, 'Training': 300, 'Recovery': -200 };
    tdee += formatAdjust[format_type] || 200;
    
    const calories = Math.max(1800, Math.round(tdee));
    
    let protein_g, carb_g, fat_g;
    if (role === 'Fast Bowler' || format_type === 'Recovery') {
      protein_g = Math.round(weight * 2.2);
      fat_g = Math.round((calories * 0.25) / 9);
    } else if (role === 'Batter' || format_type === 'Test') {
      protein_g = Math.round(weight * 1.8);
      fat_g = Math.round((calories * 0.20) / 9);
    } else {
      protein_g = Math.round(weight * 2.0);
      fat_g = Math.round((calories * 0.25) / 9);
    }
    
    carb_g = Math.round(Math.max(50, (calories - (protein_g * 4 + fat_g * 9)) / 4));
    const hydration = Math.round(((weight * 35) + (training_hours * 1000) + (role === 'Fast Bowler' ? 500 : 300)) / 100) / 10;

    return { calories, protein_g, carb_g, fat_g, hydration };
  };

  const macros = calculateMacros();

  return (
    <div className="app-container">
      
      {/* Top Banner Alert if API is disconnected */}
      {apiError && (
        <div style={{ background: 'rgba(239, 68, 68, 0.2)', border: '1px solid #ef4444', color: '#fca5a5', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span>🚨</span> <strong>System Alert:</strong> {apiError}
        </div>
      )}

      {/* Header */}
      <header>
        <div className="brand">
          <div className="brand-icon">🏏</div>
          <div className="brand-logo-text">
            <h1>CrickHealth AI</h1>
            <p>Athlete Longevity & Rehab Agent</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button 
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} 
            onClick={() => setActiveTab('overview')}
          >
            📊 Wellness & ACWR
          </button>
          <button 
            className={`tab-btn ${activeTab === 'nutrition' ? 'active' : ''}`} 
            onClick={() => setActiveTab('nutrition')}
          >
            🥑 Nutrition Coach
          </button>
          <button 
            className={`tab-btn ${activeTab === 'rehab' ? 'active' : ''}`} 
            onClick={() => setActiveTab('rehab')}
          >
            🩺 Injury Rehab
          </button>
          <button 
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`} 
            onClick={() => setActiveTab('chat')}
          >
            💬 Consult Coach
          </button>
        </nav>
      </header>

      {/* Main Layout Grid */}
      <div className="dashboard-grid">
        
        {/* Left Column - Sidebar controls */}
        <div className="sidebar">
          
          {/* Profile Card */}
          <div className="glass-card profile-card">
            <div className="profile-header">
              <div className="profile-avatar">
                {profile.role === 'Fast Bowler' ? '⚡' : profile.role === 'Batter' ? '🏏' : '🧤'}
              </div>
              <div className="profile-title">
                <h3>{profile.name}</h3>
                <span>{profile.role} • {profile.format_type} Format</span>
              </div>
            </div>

            <form onSubmit={saveProfile} className="profile-form-grid">
              <div className="form-group">
                <label>Player Name</label>
                <input 
                  type="text" 
                  value={profile.name} 
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })} 
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Cricket Role</label>
                  <select 
                    value={profile.role} 
                    onChange={(e) => setProfile({ ...profile, role: e.target.value })}
                  >
                    <option value="Fast Bowler">Fast Bowler</option>
                    <option value="Spinner">Spinner</option>
                    <option value="Batter">Batter</option>
                    <option value="Wicketkeeper">Wicketkeeper</option>
                    <option value="All-rounder">All-rounder</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Match Format</label>
                  <select 
                    value={profile.format_type} 
                    onChange={(e) => setProfile({ ...profile, format_type: e.target.value })}
                  >
                    <option value="Test">Test Match</option>
                    <option value="ODI">ODI Match</option>
                    <option value="T20">T20 Match</option>
                    <option value="Training">Training Block</option>
                    <option value="Recovery">Active Recovery</option>
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Weight (kg)</label>
                  <input 
                    type="number" 
                    step="0.1" 
                    value={profile.weight} 
                    onChange={(e) => setProfile({ ...profile, weight: parseFloat(e.target.value) || 0 })} 
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Height (cm)</label>
                  <input 
                    type="number" 
                    value={profile.height} 
                    onChange={(e) => setProfile({ ...profile, height: parseInt(e.target.value) || 0 })} 
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Age (years)</label>
                  <input 
                    type="number" 
                    value={profile.age} 
                    onChange={(e) => setProfile({ ...profile, age: parseInt(e.target.value) || 0 })} 
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Active Injury</label>
                  <select 
                    value={profile.active_injury} 
                    onChange={(e) => setProfile({ ...profile, active_injury: e.target.value })}
                  >
                    <option value="None">None (Healthy)</option>
                    <option value="shoulder_impingement">Shoulder Impingement</option>
                    <option value="lower_back_stress_fracture">Back Stress Fracture</option>
                    <option value="side_strain">Oblique Side Strain</option>
                    <option value="hamstring_strain">Hamstring Strain</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="btn-primary" style={{ marginTop: '0.5rem' }}>
                💾 Save Profile Changes
              </button>
              {profileSaved && <span className="text-success" style={{ fontSize: '0.8rem', textAlign: 'center', fontWeight: 'bold' }}>✓ Profile saved successfully!</span>}
            </form>
          </div>

          {/* Daily Logger Card */}
          <div className="glass-card">
            <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              📝 Daily Log & Workload
            </h3>
            
            {wellnessLoggedToday ? (
              <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '1rem', borderRadius: '10px', fontSize: '0.85rem', color: '#a7f3d0' }}>
                <strong>Well Done!</strong> You have logged your statistics for today. Your acute-to-chronic workload (ACWR) chart has updated.
              </div>
            ) : (
              <form onSubmit={logDailyWellness} className="wellness-section">
                <div className="form-group">
                  <div className="range-val">
                    <label>Sleep Quality</label>
                    <span>{wellnessForm.sleep_hours} hrs</span>
                  </div>
                  <input 
                    type="range" min="4" max="12" step="0.5"
                    value={wellnessForm.sleep_hours}
                    onChange={(e) => setWellnessForm({ ...wellnessForm, sleep_hours: parseFloat(e.target.value) })}
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <div className="range-val">
                      <label>Soreness</label>
                      <span>{wellnessForm.soreness_level}/10</span>
                    </div>
                    <input 
                      type="range" min="1" max="10"
                      value={wellnessForm.soreness_level}
                      onChange={(e) => setWellnessForm({ ...wellnessForm, soreness_level: parseInt(e.target.value) })}
                    />
                  </div>

                  <div className="form-group">
                    <div className="range-val">
                      <label>Fatigue</label>
                      <span>{wellnessForm.fatigue_level}/10</span>
                    </div>
                    <input 
                      type="range" min="1" max="10"
                      value={wellnessForm.fatigue_level}
                      onChange={(e) => setWellnessForm({ ...wellnessForm, fatigue_level: parseInt(e.target.value) })}
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <div className="range-val">
                      <label>Training Volume</label>
                      <span>{wellnessForm.training_hours} hrs</span>
                    </div>
                    <input 
                      type="range" min="0" max="6" step="0.5"
                      value={wellnessForm.training_hours}
                      onChange={(e) => setWellnessForm({ ...wellnessForm, training_hours: parseFloat(e.target.value) })}
                    />
                  </div>

                  <div className="form-group">
                    <div className="range-val">
                      <label>Intensity (RPE)</label>
                      <span>{wellnessForm.rpe}/10</span>
                    </div>
                    <input 
                      type="range" min="1" max="10"
                      value={wellnessForm.rpe}
                      onChange={(e) => setWellnessForm({ ...wellnessForm, rpe: parseInt(e.target.value) })}
                    />
                  </div>
                </div>

                <button type="submit" className="btn-secondary" style={{ width: '100%', marginTop: '0.5rem' }}>
                  ⚡ Submit Today's Log
                </button>
              </form>
            )}
          </div>
          
        </div>

        {/* Right Column - Tabs Container */}
        <div className="main-content">
          
          {/* Tab 1: Overview & ACWR */}
          {activeTab === 'overview' && (
            <div className="glass-card fade-in">
              <h2 style={{ marginBottom: '1.25rem' }}>🏏 Player Workload & Injury Risk</h2>
              
              {/* ACWR status banner */}
              <div className={`acwr-badge-container ${acwr.status_key || 'under'}`} style={{ backgroundColor: `rgba(${acwr.status_key === 'danger' ? '239, 68, 68' : acwr.status_key === 'optimal' ? '16, 185, 129' : acwr.status_key === 'buffer' ? '245, 158, 11' : '148, 163, 184'}, 0.08)` }}>
                <div className="acwr-score">
                  <span className="acwr-score-val" style={{ color: acwr.color_code }}>{acwr.acwr || '0.0'}</span>
                  <span className="acwr-score-label">ACWR Ratio</span>
                </div>
                <div className="acwr-info">
                  <div className="acwr-zone-title" style={{ color: acwr.color_code }}>{acwr.zone}</div>
                  <div className="acwr-risk">{acwr.risk_description}</div>
                </div>
              </div>

              {/* Chart Block */}
              <div className="chart-container">
                <div className="chart-header">
                  <h3 style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>28-Day Load Tracking Index</h3>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    Acute (last 7 days): <strong style={{ color: 'var(--primary)' }}>{acwr.acute_workload}</strong> | Chronic avg: <strong>{acwr.chronic_workload}</strong>
                  </div>
                </div>

                <div className="chart-bars">
                  {wellnessLogs.map((log, idx) => {
                    const maxVal = Math.max(...wellnessLogs.map(l => l.workload), 15);
                    const percentageHeight = (log.workload / maxVal) * 85;
                    return (
                      <div key={log.id || idx} className="chart-bar-wrapper">
                        <div className="chart-bar-tooltip">
                          Date: {log.date}<br/>Load: {log.workload} (Duration: {log.training_hours}h)
                        </div>
                        <div 
                          className="chart-bar-fill" 
                          style={{ 
                            height: `${percentageHeight}%`,
                            background: idx >= 21 
                              ? 'linear-gradient(to top, rgba(0, 210, 255, 0.4), #00d2ff)' 
                              : 'linear-gradient(to top, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.3))'
                          }}
                        ></div>
                      </div>
                    );
                  })}
                </div>
                <div className="chart-labels">
                  <span>28 Days Ago</span>
                  <span style={{ color: 'var(--primary)', fontWeight: 'bold' }}>Last 7 Days (Acute window)</span>
                  <span>Today</span>
                </div>
              </div>

              {/* Bio Feedback stats */}
              <div className="grid-2col" style={{ marginTop: '2rem' }}>
                <div className="glass-card" style={{ background: 'rgba(0,0,0,0.15)', border: '1px solid rgba(255,255,255,0.03)' }}>
                  <h4 style={{ fontSize: '0.9rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '1rem' }}>📈 Wellness Averages (Last 7 Logs)</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                      <span>Average Sleep:</span>
                      <strong style={{ color: 'var(--primary)' }}>
                        {(wellnessLogs.slice(-7).reduce((acc, curr) => acc + curr.sleep_hours, 0) / Math.max(1, Math.min(7, wellnessLogs.length))).toFixed(1)} hrs
                      </strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                      <span>Average Soreness:</span>
                      <strong style={{ color: acwr.color_code }}>
                        {(wellnessLogs.slice(-7).reduce((acc, curr) => acc + curr.soreness_level, 0) / Math.max(1, Math.min(7, wellnessLogs.length))).toFixed(1)} /10
                      </strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                      <span>Average Fatigue:</span>
                      <strong>
                        {(wellnessLogs.slice(-7).reduce((acc, curr) => acc + curr.fatigue_level, 0) / Math.max(1, Math.min(7, wellnessLogs.length))).toFixed(1)} /10
                      </strong>
                    </div>
                  </div>
                </div>

                <div className="glass-card" style={{ background: 'rgba(0,0,0,0.15)', border: '1px solid rgba(255,255,255,0.03)' }}>
                  <h4 style={{ fontSize: '0.9rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '1rem' }}>⚠️ Bowling Workload Caution</h4>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                    Fast bowler spinal stress injuries are heavily linked to acute workloads spike. Ensure you do not increase bowling spell intensity by more than 10-15% week-on-week to stay in the training **Sweet Spot**.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Tab 2: Nutrition Tab */}
          {activeTab === 'nutrition' && (
            <div className="glass-card fade-in">
              <h2 style={{ marginBottom: '1.25rem' }}>🥑 Role-Based Cricketer Nutrition</h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                Your nutritional goals are automatically customized for a <strong>{profile.role}</strong> targeting <strong>{profile.format_type}</strong> activities.
              </p>

              {/* Targets grid */}
              <div className="nutrition-grid">
                <div className="nutrition-stat">
                  <span className="nutrition-stat-val" style={{ color: 'var(--primary)' }}>{macros.calories}</span>
                  <span className="nutrition-stat-label">Daily Calories (kcal)</span>
                  <div className="nutrition-bar-outer"><div className="nutrition-bar-inner" style={{ width: '100%', backgroundColor: 'var(--primary)' }}></div></div>
                </div>

                <div className="nutrition-stat">
                  <span className="nutrition-stat-val" style={{ color: 'var(--accent)' }}>{macros.protein_g}g</span>
                  <span className="nutrition-stat-label">Protein (Tissue Repair)</span>
                  <div className="nutrition-bar-outer"><div className="nutrition-bar-inner" style={{ width: '80%', backgroundColor: 'var(--accent)' }}></div></div>
                </div>

                <div className="nutrition-stat">
                  <span className="nutrition-stat-val" style={{ color: '#f59e0b' }}>{macros.carb_g}g</span>
                  <span className="nutrition-stat-label">Carbs (Glycogen Reserve)</span>
                  <div className="nutrition-bar-outer"><div className="nutrition-bar-inner" style={{ width: '70%', backgroundColor: '#f59e0b' }}></div></div>
                </div>
              </div>

              {/* Water beaker block */}
              <div className="glass-card" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', background: 'rgba(0, 210, 255, 0.03)', borderColor: 'rgba(0, 210, 255, 0.15)', marginBottom: '1.5rem' }}>
                <span style={{ fontSize: '2.5rem' }}>💧</span>
                <div>
                  <h4 style={{ color: 'var(--primary)', fontSize: '1rem', marginBottom: '0.15rem' }}>Daily Target Hydration: {macros.hydration} Liters</h4>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Includes core metabolic hydration + 1.0L replacement per training hour + cricket gear sweat index offset (extra heavy pads and helmet heat retention).
                  </p>
                </div>
              </div>

              {/* Food recommendations */}
              <h3 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', marginTop: '1rem' }}>🛒 Recovery & Energy Grocery Guide</h3>
              <div className="foods-container">
                <div className="foods-card">
                  <h4>🍗 Premium Proteins</h4>
                  <ul className="foods-list">
                    <li>Chicken Breast & Egg Whites</li>
                    <li>Salmon / Tuna (Omega 3 anti-inflam)</li>
                    <li>Low Fat Cottage Cheese (Paneer)</li>
                    <li>Whey Protein isolate (rapid post-bowl feed)</li>
                  </ul>
                </div>

                <div className="foods-card">
                  <h4>🍠 Complex Carbs</h4>
                  <ul className="foods-list">
                    <li>Basmati Brown Rice & Oats</li>
                    <li>Sweet Potato (Steady recovery energy)</li>
                    <li>Whole Wheat Chapatis / Roti</li>
                    <li>Bananas (Electrolytes & fast digest)</li>
                  </ul>
                </div>

                <div className="foods-card" style={{ marginTop: '0.5rem' }}>
                  <h4>🥑 Joint Health Fats</h4>
                  <ul className="foods-list">
                    <li>Almonds, Walnuts & Chia seeds</li>
                    <li>Avocados & Extra Virgin Olive Oil</li>
                    <li>Natural Peanut Butter (no palm oil)</li>
                  </ul>
                </div>

                <div className="foods-card" style={{ marginTop: '0.5rem' }}>
                  <h4>💊 Cricket Specific Supplements</h4>
                  <ul className="foods-list">
                    <li>Creatine Monohydrate (fast bowling power)</li>
                    <li>Vitamin D3 & Calcium (bone density)</li>
                    <li>Electrolytes with Sodium/Potassium</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Tab 3: Injury Rehab */}
          {activeTab === 'rehab' && (
            <div className="glass-card fade-in">
              <div className="rehab-header">
                <h2>🩺 Physiotherapy & Injury Rehabilitation</h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                  Select an injury in your **Player Profile** to load a structured physical therapy and return-to-play roadmap.
                </p>
              </div>

              {!rehabGuide ? (
                <div style={{ padding: '3rem 1.5rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>🛡️</span>
                  <h3>No Active Injury Selected</h3>
                  <p style={{ fontSize: '0.85rem', marginTop: '0.5rem', maxWidth: '400px', margin: '0.5rem auto' }}>
                    Excellent news! You are currently marked as healthy. If you are recovering from side soreness, shoulder pain, or hamstring tears, update the **Active Injury** dropdown in the sidebar to generate a daily rehab checklist.
                  </p>
                </div>
              ) : (
                <div className="rehab-phase-container">
                  <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                    <h3 style={{ color: 'var(--primary)', fontSize: '1.15rem' }}>{rehabGuide.name}</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>{rehabGuide.description}</p>
                  </div>

                  {rehabGuide.phases && rehabGuide.phases.map((phase, pIdx) => (
                    <div key={pIdx} className={`rehab-phase-card ${pIdx === 0 ? 'active' : ''}`}>
                      <div className="phase-meta">
                        <span className="phase-badge">{phase.phase_name}</span>
                        <span className="phase-duration">Target: {phase.duration}</span>
                      </div>
                      
                      <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                        <strong>Phase Goals:</strong> {phase.goals.join(' • ')}
                      </div>

                      <div className="rehab-exercises-list">
                        {phase.exercises.map((ex, eIdx) => {
                          const keyName = `${rehabGuide.key}_p${pIdx}_e${eIdx}`;
                          const isCompleted = !!checkedExercises[keyName];
                          return (
                            <div 
                              key={eIdx} 
                              className={`rehab-exercise-item ${isCompleted ? 'completed' : ''}`}
                              onClick={() => toggleExercise(keyName)}
                            >
                              <div className="exercise-check-box">
                                {isCompleted ? '✓' : ''}
                              </div>
                              <div className="exercise-details">
                                <div>
                                  <span className="exercise-name">{ex.name}</span>
                                  <span className="exercise-sets-reps">{ex.sets}s x {ex.reps}</span>
                                </div>
                                <div className="exercise-notes">{ex.notes}</div>
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      <div style={{ marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        <strong>Milestone for Next Phase:</strong> {phase.milestone}
                      </div>
                    </div>
                  ))}

                  <div className="danger-box">
                    <h5>🚨 Return-to-Play Restriction Protocol:</h5>
                    <p>{rehabGuide.cricket_return_to_play}</p>
                  </div>

                  <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: '1rem', fontStyle: 'italic' }}>
                    Note: Complete these exercises under physical supervision. If pain levels exceed 3/10, terminate exercises and rest.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Tab 4: Consult AI Coach Chat */}
          {activeTab === 'chat' && (
            <div className="glass-card chat-window fade-in">
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem', marginBottom: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h2 style={{ fontSize: '1.2rem' }}>💬 AI Coach Consult Room</h2>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    Discuss diet guidelines, bio-mechanics, or shoulder/back pain queries.
                  </p>
                </div>
                <button 
                  onClick={resetAllData} 
                  style={{ background: 'transparent', border: 'none', color: '#ef4444', fontSize: '0.75rem', cursor: 'pointer', textDecoration: 'underline' }}
                >
                  Reset History
                </button>
              </div>

              {/* Chat Feed */}
              <div className="chat-messages-container">
                {messages.map((msg) => (
                  <div key={msg.id} className={`chat-bubble ${msg.sender}`}>
                    {msg.sender === 'coach' ? (
                      formatMarkdown(msg.message)
                    ) : (
                      <p>{msg.message}</p>
                    )}
                    <span className="chat-timestamp">
                      {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                ))}
                
                {chatLoading && (
                  <div className="chat-bubble coach" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                      Coach is evaluating bio-metrics and loading recovery tools...
                    </span>
                  </div>
                )}
                <div ref={chatBottomRef} />
              </div>

              {/* Chat Input */}
              <form onSubmit={sendChatMessage} className="chat-input-area">
                <input 
                  type="text" 
                  placeholder="Ask Coach: 'What should I eat?' or 'Create a lower back rehab plan'..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  disabled={chatLoading}
                />
                <button type="submit" className="btn-primary" disabled={chatLoading}>
                  Send ➔
                </button>
              </form>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}

export default App;
