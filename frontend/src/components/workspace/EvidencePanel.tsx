import React from 'react';
import { BookOpen, ChevronLeft, ChevronRight, FileText, Sparkles, ExternalLink } from 'lucide-react';
import { CitationItem } from '../../types';

interface EvidencePanelProps {
  citations: CitationItem[];
  highlightedChunkId: string | null;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({
  citations,
  highlightedChunkId,
  collapsed,
  onToggleCollapse,
}) => {
  return (
    <div
      className={`relative flex flex-col border-l border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-all duration-300 h-full ${
        collapsed ? 'w-14' : 'w-84 lg:w-96'
      }`}
    >
      {/* Panel Header */}
      <div className="flex items-center justify-between p-3.5 border-b border-slate-100 dark:border-slate-800">
        <button
          onClick={onToggleCollapse}
          title={collapsed ? 'Expand Evidence Explorer' : 'Collapse Evidence Explorer'}
          className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          {collapsed ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>

        {!collapsed && (
          <div className="flex items-center space-x-2 mr-auto ml-2">
            <BookOpen className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            <h2 className="text-sm font-semibold text-slate-900 dark:text-white">
              Evidence Explorer
            </h2>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              {citations.length}
            </span>
          </div>
        )}
      </div>

      {!collapsed ? (
        <div className="flex-1 overflow-y-auto p-3 space-y-3">
          {citations.length === 0 ? (
            <div className="text-center py-16 px-4">
              <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-3">
                <FileText className="w-5 h-5" />
              </div>
              <p className="text-xs font-medium text-slate-600 dark:text-slate-300">
                No Evidence Retrieved Yet
              </p>
              <p className="text-[11px] text-slate-400 mt-1">
                Ask a research question in the chat panel to inspect retrieved excerpts and page numbers.
              </p>
            </div>
          ) : (
            citations.map((c, idx) => {
              const isHighlighted = highlightedChunkId === c.chunk_id;
              return (
                <div
                  key={`${c.chunk_id}-${idx}`}
                  id={`evidence-${c.chunk_id}`}
                  className={`p-3.5 rounded-xl border transition-all duration-200 ${
                    isHighlighted
                      ? 'bg-amber-50/80 dark:bg-amber-950/40 border-amber-300 dark:border-amber-700 shadow-md ring-2 ring-amber-400/50'
                      : 'bg-slate-50/60 dark:bg-slate-800/40 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300">
                      Rank #{c.rank || idx + 1}
                    </span>
                    <span className="text-[11px] font-semibold text-slate-500 dark:text-slate-400">
                      Page {c.page_number}
                    </span>
                  </div>

                  <h4 className="text-xs font-bold text-slate-800 dark:text-slate-100 leading-snug line-clamp-2 mb-2">
                    {c.document_title}
                  </h4>

                  <div className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed bg-white dark:bg-slate-900/80 p-2.5 rounded-lg border border-slate-100 dark:border-slate-800/80 italic">
                    "{c.excerpt}"
                  </div>

                  <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100 dark:border-slate-800/80 text-[10px] text-slate-400">
                    <span>RRF Score: {c.score.toFixed(4)}</span>
                    <span className="font-mono text-[9px] text-slate-400 truncate max-w-[120px]">
                      {c.chunk_id}
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      ) : (
        <div className="flex-1 flex flex-col items-center py-4 space-y-3">
          <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">
            {citations.length}
          </span>
          <BookOpen className="w-5 h-5 text-slate-400" />
        </div>
      )}
    </div>
  );
};
