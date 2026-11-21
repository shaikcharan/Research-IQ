import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Send,
  Sparkles,
  Bot,
  User,
  Trash2,
  Bookmark,
  FileText,
  AlertCircle,
  HelpCircle,
  Loader2
} from 'lucide-react';
import { ChatMessage, CitationItem } from '../../types';

interface ChatPanelProps {
  messages: ChatMessage[];
  loading: boolean;
  onSendMessage: (query: string) => void;
  onClearChat: () => void;
  onSelectCitation: (chunkId: string) => void;
  selectedDocCount: number;
  onOpenSettings: () => void;
}

const SUGGESTED_QUESTIONS = [
  "What are the main challenges of electric vehicle adoption, and where do these reports disagree?",
  "Summarize the main findings across these documents.",
  "Which claims contradict each other regarding fast-charging and degradation?",
  "What limitations and missing evidence are mentioned?",
  "Compare the research methodologies and sample testing conditions.",
];

export const ChatPanel: React.FC<ChatPanelProps> = ({
  messages,
  loading,
  onSendMessage,
  onClearChat,
  onSelectCitation,
  selectedDocCount,
  onOpenSettings,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = () => {
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 dark:bg-slate-950/50 overflow-hidden">
      {/* Workspace Header Actions */}
      <div className="h-12 px-6 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between">
        <div className="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400">
          <Sparkles className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
          <span>Multi-Doc RAG Chat •</span>
          <span className="font-semibold text-slate-700 dark:text-slate-200">
            {selectedDocCount} document{selectedDocCount === 1 ? '' : 's'} active
          </span>
        </div>

        {messages.length > 0 && (
          <button
            onClick={onClearChat}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-rose-600 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Chat</span>
          </button>
        )}
      </div>

      {/* Message List */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="max-w-2xl mx-auto py-10 px-4 text-center">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mx-auto mb-4 shadow-sm border border-indigo-100 dark:border-indigo-900">
              <Bot className="w-7 h-7" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Multi-Document Research Workspace
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mb-6 leading-relaxed">
              Ask deep synthesis questions across your uploaded research papers.
              ResearchIQ retrieves evidence chunks using hybrid search (FAISS + FTS5) and synthesizes
              structured answers with verifiable page-level citations.
            </p>

            {/* Suggested prompts */}
            <div className="text-left space-y-2">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Suggested Research Inquiries:
              </p>
              <div className="grid grid-cols-1 gap-2">
                {SUGGESTED_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSendMessage(q)}
                    className="p-3 text-left text-xs text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-900 hover:bg-indigo-50 dark:hover:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700 transition-all shadow-sm flex items-start space-x-2"
                  >
                    <HelpCircle className="w-4 h-4 text-indigo-500 flex-shrink-0 mt-0.5" />
                    <span>{q}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start space-x-3.5 max-w-4xl mx-auto ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`rounded-2xl p-4.5 sm:p-5 max-w-2xl sm:max-w-3xl shadow-sm text-sm ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none ml-12'
                    : 'bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-bl-none'
                }`}
              >
                {msg.role === 'user' ? (
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                ) : (
                  <div className="space-y-4">
                    <div className="prose dark:prose-invert prose-sm max-w-none prose-headings:font-bold prose-headings:text-slate-900 dark:prose-headings:text-white prose-p:leading-relaxed prose-a:text-indigo-600 dark:prose-a:text-indigo-400">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.content}
                      </ReactMarkdown>
                    </div>

                    {/* Attached Citations Badges */}
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="pt-3 border-t border-slate-100 dark:border-slate-800">
                        <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5 text-indigo-500" />
                          <span>Retrieved Evidence Citations ({msg.citations.length}):</span>
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {msg.citations.map((cit, cIdx) => (
                            <button
                              key={`${cit.chunk_id}-${cIdx}`}
                              onClick={() => onSelectCitation(cit.chunk_id)}
                              className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-indigo-100 dark:hover:bg-indigo-950/80 hover:text-indigo-700 dark:hover:text-indigo-300 border border-slate-200 dark:border-slate-700 transition-colors text-left"
                            >
                              <span className="w-4 h-4 rounded-full bg-indigo-600 text-white text-[10px] flex items-center justify-center font-bold">
                                {cIdx + 1}
                              </span>
                              <span className="truncate max-w-[160px]">{cit.document_title}</span>
                              <span className="text-[10px] text-slate-400">p.{cit.page_number}</span>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="flex items-start space-x-3.5 max-w-4xl mx-auto">
            <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center flex-shrink-0 shadow-sm mt-1 animate-pulse">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-2xl rounded-bl-none border border-slate-200 dark:border-slate-800 shadow-sm flex items-center space-x-3 text-xs text-slate-500">
              <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
              <span>Retrieving evidence via FAISS & FTS5 and synthesizing grounded response...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-4xl mx-auto">
          {selectedDocCount === 0 && (
            <div className="mb-2 p-2 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 rounded-lg text-xs text-amber-700 dark:text-amber-300 flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>Please select at least one document in the Sources panel on the left to ask questions.</span>
            </div>
          )}

          <div className="relative flex items-end rounded-2xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-500/20 shadow-sm">
            <textarea
              rows={2}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                selectedDocCount === 0
                  ? "Select documents in the left panel to begin..."
                  : "Ask a research question across the selected papers (Enter to send, Shift+Enter for newline)..."
              }
              disabled={selectedDocCount === 0 || loading}
              className="flex-1 bg-transparent p-3.5 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none resize-none"
            />
            <div className="p-2">
              <button
                onClick={handleSend}
                disabled={!input.trim() || selectedDocCount === 0 || loading}
                className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
