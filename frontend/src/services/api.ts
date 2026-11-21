import {
  DashboardStats,
  DocumentItem,
  DocumentDetail,
  ResearchSession,
  ChatMessage,
  ComparisonResponse,
  ResearchReport,
  SettingsData,
  EvaluationBenchmark
} from '../types';

const API_BASE = '/api';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Request failed with status ${res.status}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) {
        errorDetail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      // Non-JSON error body
    }
    throw new Error(errorDetail);
  }
  return res.json();
}

export const api = {
  // System Health
  async getHealth() {
    return handleResponse<{ status: string; service: string; llm_configured: boolean }>(
      await fetch(`${API_BASE}/health`)
    );
  },

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    return handleResponse<DashboardStats>(await fetch(`${API_BASE}/dashboard/stats`));
  },

  // Documents
  async getDocuments(params?: { search?: string; status?: string; sort_by?: string; order?: string }): Promise<DocumentItem[]> {
    const query = new URLSearchParams();
    if (params?.search) query.append('search', params.search);
    if (params?.status) query.append('status', params.status);
    if (params?.sort_by) query.append('sort_by', params.sort_by);
    if (params?.order) query.append('order', params.order);
    return handleResponse<DocumentItem[]>(await fetch(`${API_BASE}/documents?${query.toString()}`));
  },

  async uploadDocuments(files: File[]): Promise<DocumentItem[]> {
    const formData = new FormData();
    for (const file of files) {
      formData.append('files', file);
    }
    return handleResponse<DocumentItem[]>(
      await fetch(`${API_BASE}/documents/upload`, {
        method: 'POST',
        body: formData,
      })
    );
  },

  async getDocumentDetail(documentId: string): Promise<DocumentDetail> {
    return handleResponse<DocumentDetail>(await fetch(`${API_BASE}/documents/${documentId}`));
  },

  async deleteDocument(documentId: string): Promise<{ message: string }> {
    return handleResponse<{ message: string }>(
      await fetch(`${API_BASE}/documents/${documentId}`, { method: 'DELETE' })
    );
  },

  async reprocessDocument(documentId: string): Promise<DocumentItem> {
    return handleResponse<DocumentItem>(
      await fetch(`${API_BASE}/documents/${documentId}/reprocess`, { method: 'POST' })
    );
  },

  async seedSampleDocuments(): Promise<DocumentItem[]> {
    return handleResponse<DocumentItem[]>(
      await fetch(`${API_BASE}/documents/seed-samples`, { method: 'POST' })
    );
  },

  // Research Sessions
  async createSession(title?: string): Promise<ResearchSession> {
    return handleResponse<ResearchSession>(
      await fetch(`${API_BASE}/research/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })
    );
  },

  async getSessions(): Promise<ResearchSession[]> {
    return handleResponse<ResearchSession[]>(await fetch(`${API_BASE}/research/sessions`));
  },

  async getSession(sessionId: string): Promise<ResearchSession> {
    return handleResponse<ResearchSession>(await fetch(`${API_BASE}/research/sessions/${sessionId}`));
  },

  async deleteSession(sessionId: string): Promise<{ message: string }> {
    return handleResponse<{ message: string }>(
      await fetch(`${API_BASE}/research/sessions/${sessionId}`, { method: 'DELETE' })
    );
  },

  async getSessionMessages(sessionId: string): Promise<ChatMessage[]> {
    return handleResponse<ChatMessage[]>(await fetch(`${API_BASE}/research/sessions/${sessionId}/messages`));
  },

  async sendChatMessage(sessionId: string, content: string, selectedDocumentIds: string[]): Promise<ChatMessage> {
    return handleResponse<ChatMessage>(
      await fetch(`${API_BASE}/research/sessions/${sessionId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, selected_document_ids: selectedDocumentIds }),
      })
    );
  },

  // Comparison
  async compareDocuments(documentIds: string[], comparisonQuestion: string): Promise<ComparisonResponse> {
    return handleResponse<ComparisonResponse>(
      await fetch(`${API_BASE}/research/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_ids: documentIds, comparison_question: comparisonQuestion }),
      })
    );
  },

  // Reports
  async generateReportDraft(
    researchQuestion: string,
    purpose: string,
    selectedDocumentIds: string[],
    title?: string
  ): Promise<{ title: string; content_markdown: string }> {
    return handleResponse<{ title: string; content_markdown: string }>(
      await fetch(`${API_BASE}/reports/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          research_question: researchQuestion,
          purpose,
          selected_document_ids: selectedDocumentIds,
          title,
        }),
      })
    );
  },

  async saveReport(
    title: string,
    researchQuestion: string,
    purpose: string,
    contentMarkdown: string,
    selectedDocumentIds: string[]
  ): Promise<ResearchReport> {
    return handleResponse<ResearchReport>(
      await fetch(`${API_BASE}/reports/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          research_question: researchQuestion,
          purpose,
          content_markdown: contentMarkdown,
          selected_document_ids: selectedDocumentIds,
        }),
      })
    );
  },

  async getReports(): Promise<ResearchReport[]> {
    return handleResponse<ResearchReport[]>(await fetch(`${API_BASE}/reports`));
  },

  async getReport(reportId: string): Promise<ResearchReport> {
    return handleResponse<ResearchReport>(await fetch(`${API_BASE}/reports/${reportId}`));
  },

  async updateReport(reportId: string, title?: string, contentMarkdown?: string): Promise<ResearchReport> {
    return handleResponse<ResearchReport>(
      await fetch(`${API_BASE}/reports/${reportId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content_markdown: contentMarkdown }),
      })
    );
  },

  async deleteReport(reportId: string): Promise<{ message: string }> {
    return handleResponse<{ message: string }>(
      await fetch(`${API_BASE}/reports/${reportId}`, { method: 'DELETE' })
    );
  },

  getReportExportUrl(reportId: string, format: 'pdf' | 'markdown'): string {
    return `${API_BASE}/reports/${reportId}/export?format=${format}`;
  },

  // Settings
  async getSettings(): Promise<SettingsData> {
    return handleResponse<SettingsData>(await fetch(`${API_BASE}/settings`));
  },

  async updateSettings(groqApiKey?: string, groqModel?: string): Promise<SettingsData> {
    return handleResponse<SettingsData>(
      await fetch(`${API_BASE}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ groq_api_key: groqApiKey, groq_model: groqModel }),
      })
    );
  },

  async testConnection(): Promise<{ success: boolean; message: string; model?: string }> {
    return handleResponse<{ success: boolean; message: string; model?: string }>(
      await fetch(`${API_BASE}/settings/test-connection`, { method: 'POST' })
    );
  },

  async rebuildIndex(): Promise<{ message: string }> {
    return handleResponse<{ message: string }>(
      await fetch(`${API_BASE}/settings/rebuild-index`, { method: 'POST' })
    );
  },

  // Evaluation
  async runBenchmark(topK: number = 5): Promise<EvaluationBenchmark> {
    return handleResponse<EvaluationBenchmark>(
      await fetch(`${API_BASE}/evaluation/benchmark?top_k=${topK}`)
    );
  },
};
