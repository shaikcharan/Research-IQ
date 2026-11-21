import React from 'react';
import {
  LayoutDashboard,
  Files,
  Sparkles,
  GitCompare,
  BookOpen,
  BarChart3,
  Settings,
  PlusCircle,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Cpu
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
  onNewSession: () => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onTabChange,
  onNewSession,
  collapsed,
  onToggleCollapse
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'documents', label: 'My Documents', icon: Files },
    { id: 'workspace', label: 'Research Workspace', icon: Sparkles },
    { id: 'compare', label: 'Compare Documents', icon: GitCompare },
    { id: 'reports', label: 'Research Reports', icon: BookOpen },
    { id: 'evaluation', label: 'Evaluation Benchmark', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside
      className={`relative flex flex-col border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-all duration-300 z-30 select-none ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-slate-100 dark:border-slate-800">
        <div
          onClick={() => onTabChange('dashboard')}
          className="flex items-center space-x-3 cursor-pointer overflow-hidden"
        >
          <div className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-700 to-violet-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <Cpu className="w-5 h-5 text-indigo-100" />
          </div>
          {!collapsed && (
            <div className="truncate">
              <span className="text-base font-bold bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-800 dark:from-white dark:to-slate-200 bg-clip-text text-transparent tracking-tight">
                ResearchIQ
              </span>
              <p className="text-[10px] uppercase font-semibold text-indigo-600 dark:text-indigo-400 tracking-wider">
                Multi-Doc RAG
              </p>
            </div>
          )}
        </div>

        <button
          onClick={onToggleCollapse}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* New Session Action */}
      <div className="p-3">
        <button
          onClick={onNewSession}
          title="Start a new research session"
          className={`w-full flex items-center justify-center space-x-2 py-2.5 px-3 rounded-xl font-medium text-sm text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 shadow-sm transition-all duration-150 ${
            collapsed ? 'px-0' : ''
          }`}
        >
          <PlusCircle className="w-4 h-4 flex-shrink-0" />
          {!collapsed && <span className="truncate">New Session</span>}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 space-y-1 overflow-y-auto pt-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              title={collapsed ? item.label : undefined}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                active
                  ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 font-semibold'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800/60'
              }`}
            >
              <Icon
                className={`w-5 h-5 flex-shrink-0 ${
                  active ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'
                }`}
              />
              {!collapsed && <span className="truncate">{item.label}</span>}
            </button>
          );
        })}
      </nav>

      {/* Footer Tagline */}
      {!collapsed && (
        <div className="p-4 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-400 dark:text-slate-500">
          <div className="flex items-center space-x-1.5 mb-1 text-slate-500 dark:text-slate-400 font-medium">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
            <span>Hybrid RAG • v1.0.0</span>
          </div>
          <p className="text-[11px] leading-tight">AI & Data Science Portfolio Project</p>
        </div>
      )}
    </aside>
  );
};
