import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DocumentItem, ChatMessage, CitationItem, ResearchSession } from '../types';
import { SourcesPanel } from '../components/workspace/SourcesPanel';
import { ChatPanel } from '../components/workspace/ChatPanel';
import { EvidencePanel } from '../components/workspace/EvidencePanel';

interface WorkspacePageProps {
  activeSession: ResearchSession | null;
  onSessionUpdated: (session: ResearchSession) => void;
  preSelectedDocIds?: string[];
  onOpenSettings: () => void;
}

export const WorkspacePage: React.FC<WorkspacePageProps> = ({
  activeSession,
  onSessionUpdated,
  preSelectedDocIds,
  onOpenSettings,
}) => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedDocIds, setSelectedDocIds] = useState<string[]>(preSelectedDocIds || []);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeCitations, setActiveCitations] = useState<CitationItem[]>([]);
  const [highlightedChunkId, setHighlightedChunkId] = useState<string | null>(null);

  // Panel collapse states
  const [leftCollapsed, setLeftCollapsed] = useState(false);
  const [rightCollapsed, setRightCollapsed] = useState(false);

  // Load documents
  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const docs = await api.getDocuments();
        setDocuments(docs);
        // By default, select all Ready documents if none selected
        if (selectedDocIds.length === 0 && docs.length > 0) {
          const readyIds = docs.filter((d) => d.processing_status === 'Ready').map((d) => d.id);
          setSelectedDocIds(readyIds);
        }
      } catch (err) {
        console.error('Failed to load documents for workspace:', err);
      }
    };
    fetchDocs();
  }, []);

  // Update selection if passed from documents page
  useEffect(() => {
    if (preSelectedDocIds && preSelectedDocIds.length > 0) {
      setSelectedDocIds(preSelectedDocIds);
    }
  }, [preSelectedDocIds]);

  // Load messages for current session
  useEffect(() => {
    if (!activeSession) return;
    const fetchMessages = async () => {
      try {
        const msgs = await api.getSessionMessages(activeSession.id);
        setMessages(msgs);
        // Set active citations to the last assistant message's citations
        const lastAssistant = [...msgs].reverse().find((m) => m.role === 'assistant');
        if (lastAssistant && lastAssistant.citations) {
          setActiveCitations(lastAssistant.citations);
        }
      } catch (err) {
        console.error('Failed to load session messages:', err);
      }
    };
    fetchMessages();
  }, [activeSession]);

  const handleToggleDoc = (docId: string) => {
    setSelectedDocIds((prev) =>
      prev.includes(docId) ? prev.filter((id) => id !== docId) : [...prev, docId]
    );
  };

  const handleSelectAll = () => {
    setSelectedDocIds(documents.map((d) => d.id));
  };

  const handleClearAll = () => {
    setSelectedDocIds([]);
  };

  const handleSendMessage = async (query: string) => {
    if (!activeSession) return;
    setLoading(true);

    // Optimistic user message display
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      session_id: activeSession.id,
      role: 'user',
      content: query,
      citations: [],
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const assistantMsg = await api.sendChatMessage(
        activeSession.id,
        query,
        selectedDocIds
      );
      setMessages((prev) => [...prev, assistantMsg]);
      if (assistantMsg.citations && assistantMsg.citations.length > 0) {
        setActiveCitations(assistantMsg.citations);
        // Expand right panel if it was collapsed
        setRightCollapsed(false);
      }
      // Update session title if updated
      const updatedSess = await api.getSession(activeSession.id);
      onSessionUpdated(updatedSess);
    } catch (err: any) {
      alert(`Synthesis Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = async () => {
    if (!activeSession) return;
    if (!confirm('Are you sure you want to clear chat messages in this session?')) return;
    try {
      // Re-create or delete session
      await api.deleteSession(activeSession.id);
      const newSess = await api.createSession('New Research Session');
      onSessionUpdated(newSess);
      setMessages([]);
      setActiveCitations([]);
    } catch (err: any) {
      alert(`Clear failed: ${err.message}`);
    }
  };

  const handleSelectCitation = (chunkId: string) => {
    setHighlightedChunkId(chunkId);
    setRightCollapsed(false);
    setTimeout(() => {
      const elem = document.getElementById(`evidence-${chunkId}`);
      if (elem) {
        elem.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  };

  return (
    <div className="flex-1 flex overflow-hidden h-[calc(100vh-4rem)]">
      {/* Left Panel: Sources */}
      <SourcesPanel
        documents={documents}
        selectedDocIds={selectedDocIds}
        onToggleDoc={handleToggleDoc}
        onSelectAll={handleSelectAll}
        onClearAll={handleClearAll}
        collapsed={leftCollapsed}
        onToggleCollapse={() => setLeftCollapsed(!leftCollapsed)}
      />

      {/* Center Panel: Research Chat */}
      <ChatPanel
        messages={messages}
        loading={loading}
        onSendMessage={handleSendMessage}
        onClearChat={handleClearChat}
        onSelectCitation={handleSelectCitation}
        selectedDocCount={selectedDocIds.length}
        onOpenSettings={onOpenSettings}
      />

      {/* Right Panel: Evidence Explorer */}
      <EvidencePanel
        citations={activeCitations}
        highlightedChunkId={highlightedChunkId}
        collapsed={rightCollapsed}
        onToggleCollapse={() => setRightCollapsed(!rightCollapsed)}
      />
    </div>
  );
};
