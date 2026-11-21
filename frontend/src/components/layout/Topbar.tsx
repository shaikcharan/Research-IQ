import React from 'react';
import { Moon, Sun, KeyRound, CheckCircle2, AlertCircle } from 'lucide-react';
import { ResearchSession } from '../../types';

interface TopbarProps {
  currentTab: string;
  activeSession: ResearchSession | null;
  llmConfigured: boolean;
  darkMode: boolean;
  onToggleDarkMode: () => void;
  onOpenSettings: () => void;
}

export const Topbar: React.FC<TopbarProps> = ({
  currentTab,
  activeSession,
  llmConfigured,
  darkMode,
  onToggleDarkMode,
  onOpenSettings,
}) => {
  const getPageTitle = () => {
    switch (currentTab) {
      case 'dashboard':
        return { title: 'Dashboard', desc: 'Real-time multi-document intelligence overview' };
      case 'documents':
        return { title: 'My Documents', desc: 'PDF library, text extraction & FAISS vector indexing' };
      case 'workspace':
        return { title: 'Research Workspace', desc: 'Evidence-grounded multi-document Q&A with citations' };
      case 'compare':
        return { title: 'Compare Documents', desc: 'Cross-document claim & contradiction analysis' };
      case 'reports':
        return { title: 'Research Reports', desc: 'Executive research briefs with citations & PDF export' };
      case 'evaluation':
        return { title: 'Evaluation Benchmark', desc: 'Empirical academic retrieval metrics (HitRate@K, Recall@K)' };
      case 'settings':
        return { title: 'Settings', desc: 'Configure Groq LLM API key, model selection & vector storage' };
      default:
        return { title: 'ResearchIQ', desc: 'Multi-document research assistant' };
    }
  };

  const pageInfo = getPageTitle();

  return (
    <header className="h-16 px-6 border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md flex items-center justify-between z-20">
      {/* Page Title & Breadcrumb */}
      <div>
        <h1 className="text-lg font-bold text-slate-900 dark:text-white leading-tight flex items-center gap-2">
          {pageInfo.title}
          {activeSession && currentTab === 'workspace' && (
            <span className="hidden sm:inline-flex items-center text-xs font-normal text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2.5 py-0.5 rounded-full border border-slate-200 dark:border-slate-700 max-w-xs truncate">
              Session: {activeSession.title}
            </span>
          )}
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 hidden md:block">
          {pageInfo.desc}
        </p>
      </div>

      {/* Action controls */}
      <div className="flex items-center space-x-3">
        {/* LLM Status Badge */}
        <button
          onClick={onOpenSettings}
          title={llmConfigured ? 'Groq LLM Connected' : 'Configure Groq API Key'}
          className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-colors ${
            llmConfigured
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800'
              : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800 hover:bg-amber-100'
          }`}
        >
          {llmConfigured ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span className="hidden sm:inline">LLM Connected</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span>Set Groq Key</span>
            </>
          )}
        </button>

        {/* Dark Mode Toggle */}
        <button
          onClick={onToggleDarkMode}
          title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          className="p-2 rounded-xl text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
        </button>

        {/* Settings Shortcut */}
        <button
          onClick={onOpenSettings}
          title="Settings"
          className="p-2 rounded-xl text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <KeyRound className="w-4 h-4" />
        </button>

        {/* User Avatar Placeholder */}
        <div
          title="Student / AI Researcher"
          className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 text-white font-semibold text-xs flex items-center justify-center ring-2 ring-white dark:ring-slate-800 shadow-sm cursor-default"
        >
          AD
        </div>
      </div>
    </header>
  );
};
