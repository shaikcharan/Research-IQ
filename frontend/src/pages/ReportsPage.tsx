import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  BookOpen,
  Sparkles,
  Download,
  Save,
  Trash2,
  Edit3,
  Eye,
  Loader2,
  CheckCircle2,
  FileText,
  CheckSquare,
  Square
} from 'lucide-react';
import { api } from '../services/api';
import { DocumentItem, ResearchReport } from '../types';
import { Modal } from '../components/common/Modal';

export const ReportsPage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [savedReports, setSavedReports] = useState<ResearchReport[]>([]);
  const [selectedDocIds, setSelectedDocIds] = useState<string[]>([]);
  const [question, setQuestion] = useState(
    'What are the commercialization bottlenecks and thermal tradeoffs in next-generation solid-state battery adoption?'
  );
  const [purpose, setPurpose] = useState('Executive Decision Making');
  const [title, setTitle] = useState('');
  const [reportMarkdown, setReportMarkdown] = useState('');
  const [generating, setGenerating] = useState(false);
  const [activeTab, setActiveTab] = useState<'editor' | 'library'>('editor');
  const [viewMode, setViewMode] = useState<'preview' | 'raw'>('preview');

  // Currently opened saved report
  const [currentReportId, setCurrentReportId] = useState<string | null>(null);
  const [reportToDelete, setReportToDelete] = useState<ResearchReport | null>(null);

  const fetchDocsAndReports = async () => {
    try {
      const [docs, reports] = await Promise.all([
        api.getDocuments(),
        api.getReports(),
      ]);
      setDocuments(docs);
      setSavedReports(reports);
      if (selectedDocIds.length === 0 && docs.length > 0) {
        setSelectedDocIds(docs.filter((d) => d.processing_status === 'Ready').map((d) => d.id));
      }
    } catch (err) {
      console.error('Failed to load documents or reports:', err);
    }
  };

  useEffect(() => {
    fetchDocsAndReports();
  }, []);

  const handleToggleDoc = (id: string) => {
    setSelectedDocIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleGenerate = async () => {
    if (selectedDocIds.length === 0) {
      alert('Please select at least one document.');
      return;
    }
    if (!question.trim()) {
      alert('Please enter a research inquiry.');
      return;
    }

    try {
      setGenerating(true);
      const res = await api.generateReportDraft(
        question.trim(),
        purpose,
        selectedDocIds,
        title || undefined
      );
      setTitle(res.title);
      setReportMarkdown(res.content_markdown);
      setCurrentReportId(null);
    } catch (err: any) {
      alert(`Generation failed: ${err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleSave = async () => {
    if (!reportMarkdown.trim()) {
      alert('Cannot save an empty report.');
      return;
    }

    try {
      const saved = await api.saveReport(
        title || `Research Brief: ${question.slice(0, 40)}`,
        question,
        purpose,
        reportMarkdown,
        selectedDocIds
      );
      setCurrentReportId(saved.id);
      await fetchDocsAndReports();
      alert('Research Brief successfully saved to SQLite database!');
    } catch (err: any) {
      alert(`Save failed: ${err.message}`);
    }
  };

  const handleOpenReport = (rep: ResearchReport) => {
    setCurrentReportId(rep.id);
    setTitle(rep.title);
    setQuestion(rep.research_question);
    setPurpose(rep.purpose);
    setReportMarkdown(rep.content_markdown);
    setSelectedDocIds(rep.selected_document_ids);
    setActiveTab('editor');
  };

  const handleDeleteReport = async () => {
    if (!reportToDelete) return;
    try {
      await api.deleteReport(reportToDelete.id);
      if (currentReportId === reportToDelete.id) {
        setCurrentReportId(null);
        setReportMarkdown('');
      }
      setReportToDelete(null);
      await fetchDocsAndReports();
    } catch (err: any) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleExport = (format: 'pdf' | 'markdown') => {
    if (!currentReportId) {
      alert('Please save the report to the database before exporting.');
      return;
    }
    const url = api.getReportExportUrl(currentReportId, format);
    window.open(url, '_blank');
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-600" />
            <span>Executive Research Brief Generator</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Produce complete 13-section academic and decision briefs backed by citations, with instant PDF and Markdown export.
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('editor')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'editor'
                ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            Report Generator & Editor
          </button>
          <button
            onClick={() => setActiveTab('library')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'library'
                ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            Saved Reports ({savedReports.length})
          </button>
        </div>
      </div>

      {activeTab === 'library' ? (
        /* Saved Reports Library */
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-4">
            Saved Research Briefs
          </h3>
          {savedReports.length === 0 ? (
            <div className="text-center py-12 text-xs text-slate-400">
              No reports saved yet. Generate a report in the editor and click Save!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {savedReports.map((rep) => (
                <div
                  key={rep.id}
                  className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700 transition space-y-3 bg-slate-50/50 dark:bg-slate-800/40"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-white line-clamp-1">
                        {rep.title}
                      </h4>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        {rep.purpose} • Saved on {new Date(rep.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={() => setReportToDelete(rep)}
                      className="p-1 rounded text-slate-400 hover:text-rose-600 transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2 italic">
                    "{rep.research_question}"
                  </p>
                  <div className="pt-2 flex items-center justify-between border-t border-slate-200 dark:border-slate-700">
                    <button
                      onClick={() => handleOpenReport(rep)}
                      className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Open & Edit</span>
                    </button>
                    <div className="flex space-x-2">
                      <a
                        href={api.getReportExportUrl(rep.id, 'markdown')}
                        target="_blank"
                        rel="noreferrer"
                        className="px-2.5 py-1 text-[11px] font-medium rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300"
                      >
                        MD
                      </a>
                      <a
                        href={api.getReportExportUrl(rep.id, 'pdf')}
                        target="_blank"
                        rel="noreferrer"
                        className="px-2.5 py-1 text-[11px] font-medium rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
                      >
                        PDF
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        /* Report Generator & In-place Editor */
        <div className="space-y-6">
          {/* Brief Configuration Card */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
                1. Select Source Documents ({selectedDocIds.length} Selected):
              </label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {documents.map((doc) => {
                  const isSelected = selectedDocIds.includes(doc.id);
                  return (
                    <div
                      key={doc.id}
                      onClick={() => handleToggleDoc(doc.id)}
                      className={`p-3 rounded-xl border cursor-pointer transition flex items-start space-x-2.5 ${
                        isSelected
                          ? 'bg-indigo-50/70 dark:bg-indigo-950/40 border-indigo-300 dark:border-indigo-700'
                          : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/40'
                      }`}
                    >
                      <button className="mt-0.5 text-indigo-600 dark:text-indigo-400 flex-shrink-0">
                        {isSelected ? (
                          <CheckSquare className="w-4 h-4" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-300 dark:text-slate-600" />
                        )}
                      </button>
                      <div className="min-w-0 flex-1">
                        <p className="text-xs font-semibold text-slate-900 dark:text-white truncate">
                          {doc.title}
                        </p>
                        <p className="text-[10px] text-slate-400 mt-0.5">
                          {doc.page_count} pgs
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                  2. Core Research Question / Thesis:
                </label>
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  className="w-full px-3.5 py-2 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                  3. Purpose / Audience:
                </label>
                <select
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  className="w-full px-3.5 py-2 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none"
                >
                  <option value="Executive Decision Making">Executive Decision Making</option>
                  <option value="Academic Literature Review">Academic Literature Review</option>
                  <option value="Technical Feasibility Analysis">Technical Feasibility Analysis</option>
                  <option value="Competitive Architecture Review">Competitive Architecture Review</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={handleGenerate}
                disabled={generating || selectedDocIds.length === 0}
                className="px-5 py-2.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 transition shadow-sm flex items-center space-x-2"
              >
                {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                <span>{generating ? 'Synthesizing 13-Section Brief...' : 'Generate Research Brief'}</span>
              </button>
            </div>
          </div>

          {/* Generated Report Editor & Preview */}
          {reportMarkdown && (
            <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Report Title..."
                  className="text-base font-bold text-slate-900 dark:text-white bg-transparent border-none focus:outline-none flex-1"
                />

                <div className="flex items-center space-x-2">
                  <div className="flex bg-slate-100 dark:bg-slate-800 p-0.5 rounded-lg mr-2">
                    <button
                      onClick={() => setViewMode('preview')}
                      className={`px-2.5 py-1 text-xs rounded-md font-medium ${
                        viewMode === 'preview'
                          ? 'bg-white dark:bg-slate-900 text-indigo-600 shadow-sm'
                          : 'text-slate-500'
                      }`}
                    >
                      Formatted Preview
                    </button>
                    <button
                      onClick={() => setViewMode('raw')}
                      className={`px-2.5 py-1 text-xs rounded-md font-medium ${
                        viewMode === 'raw'
                          ? 'bg-white dark:bg-slate-900 text-indigo-600 shadow-sm'
                          : 'text-slate-500'
                      }`}
                    >
                      Raw Markdown
                    </button>
                  </div>

                  <button
                    onClick={handleSave}
                    className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition"
                  >
                    <Save className="w-3.5 h-3.5" />
                    <span>Save to DB</span>
                  </button>

                  <button
                    onClick={() => handleExport('markdown')}
                    className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-200 transition"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>MD</span>
                  </button>

                  <button
                    onClick={() => handleExport('pdf')}
                    className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-xl text-xs font-semibold bg-rose-600 hover:bg-rose-700 text-white shadow-sm transition"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>PDF</span>
                  </button>
                </div>
              </div>

              {viewMode === 'raw' ? (
                <textarea
                  rows={20}
                  value={reportMarkdown}
                  onChange={(e) => setReportMarkdown(e.target.value)}
                  className="w-full font-mono text-xs p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              ) : (
                <div className="prose dark:prose-invert prose-sm max-w-none p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {reportMarkdown}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={!!reportToDelete}
        onClose={() => setReportToDelete(null)}
        title="Delete Saved Report"
        maxWidth="md"
      >
        {reportToDelete && (
          <div className="space-y-4 text-xs">
            <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
              Are you sure you want to delete <strong className="text-slate-900 dark:text-white">{reportToDelete.title}</strong>?
              This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3 pt-2">
              <button
                onClick={() => setReportToDelete(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold hover:bg-slate-100 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteReport}
                className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-semibold transition"
              >
                Confirm Delete
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};
