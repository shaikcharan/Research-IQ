import React, { useState, useEffect } from 'react';
import {
  Settings,
  KeyRound,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  RefreshCw,
  Database,
  Cpu,
  Save,
  Loader2,
  Eye,
  EyeOff
} from 'lucide-react';
import { api } from '../services/api';
import { SettingsData } from '../types';

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('llama-3.3-70b-versatile');
  const [showKey, setShowKey] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);

  const fetchSettings = async () => {
    try {
      const data = await api.getSettings();
      setSettings(data);
      setModel(data.groq_model);
    } catch (err) {
      console.error('Failed to load settings:', err);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleSave = async () => {
    try {
      setSaving(true);
      await api.updateSettings(apiKey || undefined, model);
      await fetchSettings();
      setApiKey('');
      alert('Settings saved and persisted to backend environment successfully!');
    } catch (err: any) {
      alert(`Save failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setTestResult(null);
      const res = await api.testConnection();
      setTestResult(res);
    } catch (err: any) {
      setTestResult({ success: false, message: err.message || 'Connection test failed.' });
    } finally {
      setTesting(false);
    }
  };

  const handleRebuildIndex = async () => {
    if (!confirm('Rebuild FAISS index and FTS5 table from database chunks?')) return;
    try {
      setRebuilding(true);
      const res = await api.rebuildIndex();
      alert(res.message);
      await fetchSettings();
    } catch (err: any) {
      alert(`Rebuild failed: ${err.message}`);
    } finally {
      setRebuilding(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6 max-w-5xl mx-auto">
      <div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Settings className="w-5 h-5 text-indigo-600" />
          <span>System Settings & LLM Configuration</span>
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Configure the Groq Cloud LLM provider, manage embedding parameters, and verify vector storage health.
        </p>
      </div>

      {/* LLM Key Configuration Card */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center space-x-2">
            <KeyRound className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">
              Groq Cloud LLM API Key
            </h3>
          </div>
          <span
            className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${
              settings?.groq_api_key_configured
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-400'
                : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950 dark:text-amber-400'
            }`}
          >
            {settings?.groq_api_key_configured ? 'Key Configured (Active)' : 'Key Missing'}
          </span>
        </div>

        <div className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-800/40 p-4 rounded-xl border border-slate-100 dark:border-slate-800 space-y-2">
          <p>
            ResearchIQ uses the ultrafast <strong>Groq Cloud API</strong> for evidence synthesis, contradiction analysis,
            and executive brief generation. PDF ingestion, sentence chunking, Sentence-Transformers embeddings,
            and FAISS hybrid retrieval operate 100% locally on your machine without requiring an API key.
          </p>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold">
            <ExternalLink className="w-3.5 h-3.5" />
            <a
              href="https://console.groq.com/keys"
              target="_blank"
              rel="noreferrer"
              className="hover:underline"
            >
              Get a Free Groq API Key at console.groq.com
            </a>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
              Groq API Key (Stored Server-Side in .env):
            </label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={settings?.groq_api_key_configured ? '•••••••••••••••••••••••• (Leave blank to keep existing)' : 'Enter gsk_... key'}
                className="w-full px-3.5 py-2.5 pr-10 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
              Synthesis Model:
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3.5 py-2.5 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none font-medium"
            >
              <option value="llama-3.3-70b-versatile">llama-3.3-70b-versatile (Recommended • Deep Reasoning)</option>
              <option value="llama-3.1-8b-instant">llama-3.1-8b-instant (Fastest • Lightweight)</option>
              <option value="mixtral-8x7b-32768">mixtral-8x7b-32768 (High Context Window)</option>
            </select>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <button
              onClick={handleTestConnection}
              disabled={testing}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition flex items-center space-x-2"
            >
              {testing ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
              <span>Test Connection</span>
            </button>

            <button
              onClick={handleSave}
              disabled={saving}
              className="px-5 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white transition shadow-sm flex items-center space-x-2"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              <span>Save Settings</span>
            </button>
          </div>

          {testResult && (
            <div
              className={`p-3.5 rounded-xl border text-xs flex items-center space-x-2.5 ${
                testResult.success
                  ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 text-emerald-700 dark:text-emerald-400'
                  : 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 text-rose-700 dark:text-rose-400'
              }`}
            >
              {testResult.success ? (
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
              )}
              <span>{testResult.message}</span>
            </div>
          )}
        </div>
      </div>

      {/* Storage and Vector Database Health */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center space-x-2">
            <Database className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">
              Vector Storage & Hybrid Engine Diagnostics
            </h3>
          </div>
          <button
            onClick={handleRebuildIndex}
            disabled={rebuilding}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-800 transition flex items-center space-x-1.5"
          >
            {rebuilding ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
            <span>Rebuild Vector Index</span>
          </button>
        </div>

        {settings && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl">
              <span className="text-slate-400">Embedding Model:</span>
              <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5 truncate">
                {settings.embedding_model.split('/').pop()}
              </p>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl">
              <span className="text-slate-400">Vector Dimension:</span>
              <p className="font-semibold text-indigo-600 dark:text-indigo-400 mt-0.5">
                384 (Cosine Inner Product)
              </p>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl">
              <span className="text-slate-400">Total Indexed Chunks:</span>
              <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">
                {settings.total_chunks} chunks
              </p>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl">
              <span className="text-slate-400">Max Upload Size:</span>
              <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">
                {settings.max_upload_mb} MB per file
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
