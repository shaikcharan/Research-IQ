import React, { useEffect, useState } from 'react';
import {
  Files,
  CheckCircle2,
  Brain,
  BookOpen,
  ArrowRight,
  Upload,
  Sparkles,
  GitCompare,
  Layers,
  Clock,
  FileText,
  AlertCircle
} from 'lucide-react';
import { api } from '../services/api';
import { DashboardStats } from '../types';
import { Badge } from '../components/common/Badge';

interface DashboardPageProps {
  onNavigate: (tab: string) => void;
  onSelectSession: (sessionId: string) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  onNavigate,
  onSelectSession
}) => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [seeding, setSeeding] = useState(false);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      setStats(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch dashboard metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleSeedSamples = async () => {
    try {
      setSeeding(true);
      await api.seedSampleDocuments();
      await fetchStats();
    } catch (err: any) {
      alert(`Failed to seed sample papers: ${err.message}`);
    } finally {
      setSeeding(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500">Loading ResearchIQ metrics from database...</p>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-8">
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-xl text-rose-700 dark:text-rose-400 text-sm flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error || 'Unable to load dashboard data.'}</span>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      label: 'Total Documents',
      value: stats.total_documents,
      icon: Files,
      color: 'text-blue-600',
      bg: 'bg-blue-50 dark:bg-blue-950/50',
    },
    {
      label: 'Indexed (FAISS + FTS5)',
      value: stats.indexed_documents,
      icon: CheckCircle2,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50 dark:bg-emerald-950/50',
    },
    {
      label: 'Research Sessions',
      value: stats.total_sessions,
      icon: Brain,
      color: 'text-indigo-600',
      bg: 'bg-indigo-50 dark:bg-indigo-950/50',
    },
    {
      label: 'Saved Reports',
      value: stats.total_reports,
      icon: BookOpen,
      color: 'text-violet-600',
      bg: 'bg-violet-50 dark:bg-violet-950/50',
    },
  ];

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-8 max-w-7xl mx-auto">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-8 text-white shadow-xl border border-slate-800">
        <div className="relative z-10 max-w-2xl space-y-3">
          <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Academic & Industrial Research Intelligence</span>
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            ResearchIQ Assistant
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Upload multiple research papers, compare conflicting scientific claims, query across documents
            with Reciprocal Rank Fusion hybrid retrieval, and generate structured executive research briefs.
          </p>
          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate('workspace')}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 transition shadow-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span>Open Workspace</span>
            </button>
            <button
              onClick={() => onNavigate('documents')}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 transition text-white border border-white/20"
            >
              <Upload className="w-4 h-4" />
              <span>Upload Documents</span>
            </button>
            {stats.total_documents === 0 && (
              <button
                onClick={handleSeedSamples}
                disabled={seeding}
                className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-600/80 hover:bg-emerald-600 transition text-white"
              >
                <Layers className="w-4 h-4" />
                <span>{seeding ? 'Seeding Papers...' : 'Seed Sample Papers (1-Click)'}</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div
              key={i}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center space-x-4"
            >
              <div className={`p-3.5 rounded-2xl ${card.bg}`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
                  {card.label}
                </p>
                <p className="text-2xl font-bold text-slate-900 dark:text-white mt-0.5">
                  {card.value}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Launch Cards */}
      <div>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
          Research Capabilities
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            onClick={() => onNavigate('workspace')}
            className="group p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700 hover:shadow-md transition cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 flex items-center justify-center mb-3">
              <Sparkles className="w-5 h-5" />
            </div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              Multi-Doc Workspace
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 transition" />
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">
              Query multiple selected papers simultaneously with hybrid dense/sparse search and exact page citations.
            </p>
          </div>

          <div
            onClick={() => onNavigate('compare')}
            className="group p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-violet-300 dark:hover:border-violet-700 hover:shadow-md transition cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-violet-50 dark:bg-violet-950/60 text-violet-600 flex items-center justify-center mb-3">
              <GitCompare className="w-5 h-5" />
            </div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              Contradiction Analysis
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-violet-600 transition" />
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">
              Detect conflicting empirical claims, sample variations, and methodology differences across studies.
            </p>
          </div>

          <div
            onClick={() => onNavigate('reports')}
            className="group p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-emerald-300 dark:hover:border-emerald-700 hover:shadow-md transition cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 flex items-center justify-center mb-3">
              <BookOpen className="w-5 h-5" />
            </div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              Executive Brief Synthesis
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 transition" />
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">
              Generate 13-section structured research briefs and export directly to clean Markdown and PDF.
            </p>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Recent Documents & Recent Sessions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Uploads */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Files className="w-4 h-4 text-indigo-600" />
              <span>Recent Documents</span>
            </h3>
            <button
              onClick={() => onNavigate('documents')}
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-700"
            >
              View All ({stats.total_documents})
            </button>
          </div>

          <div className="divide-y divide-slate-100 dark:divide-slate-800 mt-2">
            {stats.recent_documents.length === 0 ? (
              <div className="text-center py-8 text-xs text-slate-400">
                No documents uploaded yet. Go to My Documents to upload research PDFs.
              </div>
            ) : (
              stats.recent_documents.map((doc) => (
                <div key={doc.id} className="py-3 flex items-center justify-between">
                  <div className="min-w-0 pr-3">
                    <p className="text-xs font-semibold text-slate-900 dark:text-white truncate">
                      {doc.title}
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {doc.page_count} pages • {(doc.file_size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <Badge variant={doc.processing_status === 'Ready' ? 'ready' : 'indexing'}>
                    {doc.processing_status}
                  </Badge>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-indigo-600" />
              <span>Recent Research Sessions</span>
            </h3>
            <button
              onClick={() => onNavigate('workspace')}
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-700"
            >
              Open Workspace
            </button>
          </div>

          <div className="divide-y divide-slate-100 dark:divide-slate-800 mt-2">
            {stats.recent_sessions.length === 0 ? (
              <div className="text-center py-8 text-xs text-slate-400">
                No research sessions yet. Start a new session from the sidebar!
              </div>
            ) : (
              stats.recent_sessions.map((sess) => (
                <div
                  key={sess.id}
                  onClick={() => {
                    onSelectSession(sess.id);
                    onNavigate('workspace');
                  }}
                  className="py-3 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-800/40 px-2 rounded-xl cursor-pointer transition"
                >
                  <div className="min-w-0 pr-3">
                    <p className="text-xs font-semibold text-slate-900 dark:text-white truncate">
                      {sess.title}
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {sess.message_count} messages • Active {new Date(sess.updated_at).toLocaleDateString()}
                    </p>
                  </div>
                  <ArrowRight className="w-4 h-4 text-slate-300" />
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
