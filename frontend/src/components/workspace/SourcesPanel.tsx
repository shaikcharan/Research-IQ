import React, { useState } from 'react';
import { Search, CheckSquare, Square, FileText, ChevronLeft, ChevronRight } from 'lucide-react';
import { DocumentItem } from '../../types';
import { Badge } from '../common/Badge';

interface SourcesPanelProps {
  documents: DocumentItem[];
  selectedDocIds: string[];
  onToggleDoc: (id: string) => void;
  onSelectAll: () => void;
  onClearAll: () => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const SourcesPanel: React.FC<SourcesPanelProps> = ({
  documents,
  selectedDocIds,
  onToggleDoc,
  onSelectAll,
  onClearAll,
  collapsed,
  onToggleCollapse,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredDocs = documents.filter((d) =>
    d.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div
      className={`relative flex flex-col border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-all duration-300 h-full ${
        collapsed ? 'w-14' : 'w-80'
      }`}
    >
      {/* Panel Header */}
      <div className="flex items-center justify-between p-3.5 border-b border-slate-100 dark:border-slate-800">
        {!collapsed && (
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-sm font-semibold text-slate-900 dark:text-white">
                Sources
              </h2>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400">
                {selectedDocIds.length} / {documents.length}
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Select papers for multi-doc RAG</p>
          </div>
        )}
        <button
          onClick={onToggleCollapse}
          title={collapsed ? 'Expand Sources' : 'Collapse Sources'}
          className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors ml-auto"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {!collapsed && (
        <>
          {/* Search bar & quick select */}
          <div className="p-3 space-y-2 border-b border-slate-100 dark:border-slate-800">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search documents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="flex items-center justify-between text-xs text-indigo-600 dark:text-indigo-400 pt-0.5">
              <button
                onClick={onSelectAll}
                className="hover:underline font-medium"
              >
                Select All
              </button>
              <button
                onClick={onClearAll}
                className="hover:underline font-medium text-slate-500 hover:text-slate-700 dark:text-slate-400"
              >
                Clear
              </button>
            </div>
          </div>

          {/* Document list */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {filteredDocs.length === 0 ? (
              <div className="text-center py-8 text-xs text-slate-400">
                No matching documents found.
              </div>
            ) : (
              filteredDocs.map((doc) => {
                const isSelected = selectedDocIds.includes(doc.id);
                return (
                  <div
                    key={doc.id}
                    onClick={() => onToggleDoc(doc.id)}
                    className={`flex items-start space-x-2.5 p-2.5 rounded-xl cursor-pointer transition-colors border ${
                      isSelected
                        ? 'bg-indigo-50/70 dark:bg-indigo-950/40 border-indigo-200 dark:border-indigo-800'
                        : 'border-transparent hover:bg-slate-50 dark:hover:bg-slate-800/50'
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
                      <div className="flex items-center space-x-2 mt-1 text-[11px] text-slate-400">
                        <span className="flex items-center">
                          <FileText className="w-3 h-3 mr-0.5" />
                          {doc.page_count} pgs
                        </span>
                        <span>•</span>
                        <Badge
                          variant={doc.processing_status === 'Ready' ? 'ready' : 'indexing'}
                          className="text-[10px] py-0 px-1.5"
                        >
                          {doc.processing_status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </>
      )}

      {collapsed && (
        <div className="flex-1 flex flex-col items-center py-4 space-y-3">
          <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">
            {selectedDocIds.length}
          </span>
          <FileText className="w-5 h-5 text-slate-400" />
        </div>
      )}
    </div>
  );
};
