export interface DocumentItem {
  id: string;
  filename: string;
  title: string;
  file_size: number;
  page_count: number;
  processing_status: 'Uploaded' | 'Extracting' | 'Indexing' | 'Ready' | 'Failed';
  processing_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  chunk_index: number;
  page_number: number;
  text: string;
}

export interface DocumentDetail extends DocumentItem {
  chunks_count: number;
  sample_chunks: DocumentChunk[];
}

export interface DashboardStats {
  total_documents: number;
  indexed_documents: number;
  total_sessions: number;
  total_reports: number;
  total_chunks: number;
  recent_documents: DocumentItem[];
  recent_sessions: {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    message_count: number;
  }[];
}

export interface CitationItem {
  chunk_id: string;
  document_id: string;
  document_title: string;
  page_number: number;
  excerpt: string;
  score: number;
  rank?: number;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  citations: CitationItem[];
  created_at: string;
}

export interface ResearchSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ComparisonItem {
  topic: string;
  document_a_evidence: string;
  document_b_evidence: string;
  relationship: 'Agreement' | 'Difference' | 'Potential Contradiction' | 'Insufficient Evidence';
  citations: CitationItem[];
  explanation: string;
  human_review_recommended: boolean;
}

export interface ComparisonResponse {
  question: string;
  documents_compared: { id: string; title: string }[];
  comparisons: ComparisonItem[];
  summary: string;
}

export interface ResearchReport {
  id: string;
  title: string;
  research_question: string;
  purpose: string;
  content_markdown: string;
  selected_document_ids: string[];
  created_at: string;
  updated_at: string;
}

export interface SettingsData {
  groq_api_key_configured: boolean;
  groq_model: string;
  app_host: string;
  app_port: number;
  max_upload_mb: number;
  embedding_model: string;
  total_indexed_documents: number;
  total_chunks: number;
}

export interface EvaluationResult {
  query: string;
  expected_docs: string[];
  retrieved_docs: string[];
  hit: boolean;
  recall: number;
  citation_coverage: number;
  faithfulness: string;
}

export interface EvaluationBenchmark {
  total_queries: number;
  hit_rate_at_k: number;
  average_recall: number;
  average_citation_coverage: number;
  results: EvaluationResult[];
  explanation: Record<string, string>;
}
