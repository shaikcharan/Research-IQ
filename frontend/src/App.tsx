import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Topbar } from './components/layout/Topbar';
import { DashboardPage } from './pages/DashboardPage';
import { DocumentsPage } from './pages/DocumentsPage';
import { WorkspacePage } from './pages/WorkspacePage';
import { ComparePage } from './pages/ComparePage';
import { ReportsPage } from './pages/ReportsPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { api } from './services/api';
import { ResearchSession } from './types';

export function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeSession, setActiveSession] = useState<ResearchSession | null>(null);
  const [preSelectedDocIds, setPreSelectedDocIds] = useState<string[]>([]);
  const [llmConfigured, setLlmConfigured] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('researchiq_theme') === 'dark';
  });

  // Apply dark mode to document
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('researchiq_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('researchiq_theme', 'light');
    }
  }, [darkMode]);

  // Check LLM config and load/initialize sessions
  useEffect(() => {
    const initApp = async () => {
      try {
        const health = await api.getHealth();
        setLlmConfigured(health.llm_configured);

        const sessions = await api.getSessions();
        if (sessions.length > 0) {
          setActiveSession(sessions[0]);
        } else {
          const newSess = await api.createSession('New Research Session');
          setActiveSession(newSess);
        }
      } catch (err) {
        console.error('App init error:', err);
      }
    };
    initApp();
  }, []);

  const handleNewSession = async () => {
    try {
      const newSess = await api.createSession('New Research Session');
      setActiveSession(newSess);
      setCurrentTab('workspace');
    } catch (err: any) {
      alert(`Could not create new session: ${err.message}`);
    }
  };

  const handleStartResearch = (docIds: string[]) => {
    setPreSelectedDocIds(docIds);
    setCurrentTab('workspace');
  };

  const handleSelectSession = async (sessionId: string) => {
    try {
      const sess = await api.getSession(sessionId);
      setActiveSession(sess);
    } catch (err) {
      console.error('Failed to switch session:', err);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 font-sans">
      {/* Persistent Sidebar */}
      <Sidebar
        currentTab={currentTab}
        onTabChange={setCurrentTab}
        onNewSession={handleNewSession}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <Topbar
          currentTab={currentTab}
          activeSession={activeSession}
          llmConfigured={llmConfigured}
          darkMode={darkMode}
          onToggleDarkMode={() => setDarkMode(!darkMode)}
          onOpenSettings={() => setCurrentTab('settings')}
        />

        {/* Page Content */}
        <main className="flex-1 flex overflow-hidden">
          {currentTab === 'dashboard' && (
            <DashboardPage
              onNavigate={setCurrentTab}
              onSelectSession={handleSelectSession}
            />
          )}

          {currentTab === 'documents' && (
            <DocumentsPage onStartResearch={handleStartResearch} />
          )}

          {currentTab === 'workspace' && (
            <WorkspacePage
              activeSession={activeSession}
              onSessionUpdated={setActiveSession}
              preSelectedDocIds={preSelectedDocIds}
              onOpenSettings={() => setCurrentTab('settings')}
            />
          )}

          {currentTab === 'compare' && <ComparePage />}

          {currentTab === 'reports' && <ReportsPage />}

          {currentTab === 'evaluation' && <EvaluationPage />}

          {currentTab === 'settings' && <SettingsPage />}
        </main>
      </div>
    </div>
  );
}

export default App;
