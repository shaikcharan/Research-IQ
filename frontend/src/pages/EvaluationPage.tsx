import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  Award,
  CheckCircle2,
  HelpCircle,
  Play,
  Loader2,
  FileText,
  Info,
  ShieldCheck
} from 'lucide-react';
import { api } from '../services/api';
import { EvaluationBenchmark } from '../types';

export const EvaluationPage: React.FC = () => {
  const [benchmark, setBenchmark] = useState<EvaluationBenchmark | null>(null);
  const [loading, setLoading] = useState(false);
  const [topK, setTopK] = useState(5);

  const runEvaluation = async () => {
    try {
      setLoading(true);
      const data = await api.runBenchmark(topK);
      setBenchmark(data);
    } catch (err: any) {
      alert(`Benchmark failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runEvaluation();
  }, []);

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-600" />
            <span>Academic Retrieval Evaluation & Benchmark</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Empirical evaluation suite measuring RAG retrieval accuracy, keyword recall, and citation faithfulness.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-300">
            <span>Cutoff K:</span>
            <select
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-semibold"
            >
              <option value={3}>K = 3</option>
              <option value={5}>K = 5</option>
              <option value={8}>K = 8</option>
            </select>
          </div>

          <button
            onClick={runEvaluation}
            disabled={loading}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 transition shadow-sm flex items-center space-x-2"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            <span>Run Benchmark</span>
          </button>
        </div>
      </div>

      {/* Metrics Cards */}
      {benchmark && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Retrieval Hit Rate@{topK}
            </span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-3xl font-extrabold text-indigo-600 dark:text-indigo-400">
                {(benchmark.hit_rate_at_k * 100).toFixed(0)}%
              </span>
              <span className="text-xs text-slate-400">
                ({benchmark.results.filter((r) => r.hit).length} / {benchmark.total_queries} queries)
              </span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-2">
              Fraction of inquiries with relevant evidence surfaced in top-{topK}.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Mean Recall@{topK}
            </span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">
                {(benchmark.average_recall * 100).toFixed(1)}%
              </span>
              <span className="text-xs text-slate-400">topic vector recall</span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-2">
              Proportion of key experimental topics matched in retrieved context.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Citation Coverage
            </span>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-3xl font-extrabold text-violet-600 dark:text-violet-400">
                {benchmark.average_citation_coverage.toFixed(1)}%
              </span>
              <span className="text-xs text-slate-400">verifiable claims</span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-2">
              Percentage of retrieved claims accompanied by 1-indexed page citations.
            </p>
          </div>
        </div>
      )}

      {/* Query-by-Query Evaluation Breakdown */}
      {benchmark && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Evaluation Test Dataset & Results
            </h3>
            <span className="text-xs font-semibold text-slate-400">
              {benchmark.results.length} Queries Evaluated
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-800/40 text-slate-400 font-semibold">
                  <th className="p-4">Research Query</th>
                  <th className="p-4">Retrieved Papers</th>
                  <th className="p-4">Hit</th>
                  <th className="p-4">Recall@{topK}</th>
                  <th className="p-4">Citation Coverage</th>
                  <th className="p-4">Faithfulness</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {benchmark.results.map((res, i) => (
                  <tr key={i} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition">
                    <td className="p-4 font-semibold text-slate-900 dark:text-white max-w-sm">
                      {res.query}
                    </td>
                    <td className="p-4 text-slate-600 dark:text-slate-300">
                      {res.retrieved_docs.length > 0
                        ? res.retrieved_docs.join(', ')
                        : 'No documents matched'}
                    </td>
                    <td className="p-4">
                      {res.hit ? (
                        <span className="inline-flex items-center text-emerald-600 font-semibold">
                          <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Yes
                        </span>
                      ) : (
                        <span className="text-rose-500 font-semibold">No</span>
                      )}
                    </td>
                    <td className="p-4 font-semibold text-slate-700 dark:text-slate-300">
                      {(res.recall * 100).toFixed(0)}%
                    </td>
                    <td className="p-4 font-semibold text-indigo-600 dark:text-indigo-400">
                      {res.citation_coverage}%
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                        {res.faithfulness}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Academic Methodology & Metric Definitions Guide */}
      <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Info className="w-4 h-4 text-indigo-600" />
          <span>Academic Evaluation Methodology & Limitations (For Project Presentation)</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 space-y-1.5">
            <h4 className="font-bold text-slate-800 dark:text-slate-100">
              1. Hit Rate@K & Recall@K
            </h4>
            <p>
              Hit Rate@K measures whether at least one relevant passage was retrieved in the top-K ranking.
              Recall@K calculates the proportion of target factual topics and technical terms present in the retrieved context window.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 space-y-1.5">
            <h4 className="font-bold text-slate-800 dark:text-slate-100">
              2. Citation Coverage & Grounding
            </h4>
            <p>
              Citation coverage quantifies the percentage of synthesized statements backed by document IDs and original PDF page numbers.
              This guarantees that claims are grounded in verifiable source literature rather than LLM parametric hallucinations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
