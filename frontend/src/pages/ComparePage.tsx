import React, { useState, useEffect } from 'react';
import {
  GitCompare,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  FileText,
  Download,
  Loader2,
  CheckSquare,
  Square
} from 'lucide-react';
import { api } from '../services/api';
import { DocumentItem, ComparisonResponse } from '../types';
import { Badge } from '../components/common/Badge';

export const ComparePage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedDocIds, setSelectedDocIds] = useState<string[]>([]);
  const [question, setQuestion] = useState(
    'What are the degradation limits and temperature recommendations during fast charging, and where do these papers disagree?'
  );
  const [loading, setLoading] = useState(false);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const docs = await api.getDocuments();
        setDocuments(docs);
        const ready = docs.filter((d) => d.processing_status === 'Ready');
        // Pre-select first 2 ready docs
        if (ready.length >= 2) {
          setSelectedDocIds([ready[0].id, ready[1].id]);
        }
      } catch (err) {
        console.error('Failed to load documents:', err);
      }
    };
    fetchDocs();
  }, []);

  const handleToggleDoc = (id: string) => {
    setSelectedDocIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleRunComparison = async () => {
    if (selectedDocIds.length < 2) {
      alert('Please select at least 2 documents to compare.');
      return;
    }
    if (!question.trim()) {
      alert('Please enter a comparison inquiry.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const res = await api.compareDocuments(selectedDocIds, question.trim());
      setComparisonResult(res);
    } catch (err: any) {
      setError(err.message || 'Comparison failed.');
    } finally {
      setLoading(false);
    }
  };

  const exportComparisonMarkdown = () => {
    if (!comparisonResult) return;
    let md = `# Comparative Research Analysis\n\n`;
    md += `**Inquiry:** ${comparisonResult.question}\n\n`;
    md += `**Documents Analyzed:**\n`;
    comparisonResult.documents_compared.forEach((d) => {
      md += `- ${d.title}\n`;
    });
    md += `\n## Executive Summary\n${comparisonResult.summary}\n\n`;
    md += `## Claim Comparison & Contradiction Matrix\n\n`;
    md += `| Topic | Document Evidence | Relationship | Explanation |\n`;
    md += `|---|---|---|---|\n`;
    comparisonResult.comparisons.forEach((c) => {
      md += `| **${c.topic}** | **Doc A:** ${c.document_a_evidence}<br>**Doc B:** ${c.document_b_evidence} | ${c.relationship} | ${c.explanation} |\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comparative_analysis_${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <GitCompare className="w-5 h-5 text-violet-600" />
          <span>Cross-Document Comparison & Contradiction Analysis</span>
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Select two or more papers to evaluate empirical discrepancies, cycle life conflicts, and methodology divergences.
        </p>
      </div>

      {/* Configuration Card */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
        <div>
          <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
            1. Select Papers to Compare (Minimum 2):
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {documents.map((doc) => {
              const isSelected = selectedDocIds.includes(doc.id);
              return (
                <div
                  key={doc.id}
                  onClick={() => handleToggleDoc(doc.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition flex items-start space-x-3 ${
                    isSelected
                      ? 'bg-violet-50/70 dark:bg-violet-950/40 border-violet-300 dark:border-violet-700'
                      : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/40'
                  }`}
                >
                  <button className="mt-0.5 text-violet-600 dark:text-violet-400 flex-shrink-0">
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
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {doc.page_count} pages • {doc.processing_status}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
            2. Comparison Question / Target Dimension:
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. Where do these reports disagree regarding battery degradation and costs?"
              className="flex-1 px-4 py-2.5 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
            />
            <button
              onClick={handleRunComparison}
              disabled={loading || selectedDocIds.length < 2}
              className="px-5 py-2.5 rounded-xl text-xs font-semibold bg-violet-600 hover:bg-violet-700 text-white disabled:opacity-50 transition shadow-sm flex items-center space-x-2 flex-shrink-0"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              <span>{loading ? 'Analyzing Claims...' : 'Run Comparative Analysis'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-xl text-xs text-rose-700 dark:text-rose-400 flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results View */}
      {comparisonResult && (
        <div className="space-y-6">
          {/* Summary Banner */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Synthesis Findings & Discrepancy Overview</span>
              </h3>
              <button
                onClick={exportComparisonMarkdown}
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Markdown</span>
              </button>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              {comparisonResult.summary}
            </p>
          </div>

          {/* Detailed Matrix Table */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
            <div className="p-4 border-b border-slate-100 dark:border-slate-800">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Claim Comparison Matrix ({comparisonResult.comparisons.length} Extracted Claims)
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-800/40 text-slate-400 font-semibold">
                    <th className="p-4 w-44">Topic / Claim</th>
                    <th className="p-4">Document Evidence</th>
                    <th className="p-4 w-36">Relationship</th>
                    <th className="p-4 w-72">Comparative Explanation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {comparisonResult.comparisons.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/30 transition">
                      <td className="p-4 font-bold text-slate-900 dark:text-white align-top">
                        {item.topic}
                        {item.human_review_recommended && (
                          <span className="block mt-1 text-[10px] font-normal text-amber-600">
                            * Human review recommended
                          </span>
                        )}
                      </td>
                      <td className="p-4 space-y-2 align-top">
                        <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                          <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 block mb-0.5">
                            Doc A Claim:
                          </span>
                          <p className="text-slate-700 dark:text-slate-200 italic leading-relaxed">
                            "{item.document_a_evidence}"
                          </p>
                        </div>
                        <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                          <span className="text-[10px] font-bold text-violet-600 dark:text-violet-400 block mb-0.5">
                            Doc B Claim:
                          </span>
                          <p className="text-slate-700 dark:text-slate-200 italic leading-relaxed">
                            "{item.document_b_evidence}"
                          </p>
                        </div>
                      </td>
                      <td className="p-4 align-top">
                        <Badge
                          variant={
                            item.relationship === 'Agreement'
                              ? 'agreement'
                              : item.relationship === 'Potential Contradiction'
                              ? 'contradiction'
                              : item.relationship === 'Difference'
                              ? 'difference'
                              : 'insufficient'
                          }
                        >
                          {item.relationship}
                        </Badge>
                      </td>
                      <td className="p-4 text-slate-600 dark:text-slate-300 leading-relaxed align-top">
                        {item.explanation}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
