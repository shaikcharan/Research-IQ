from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# -----------------
# Document Models
# -----------------
class DocumentResponse(BaseModel):
    id: str
    filename: str
    title: str
    file_size: int
    page_count: int
    processing_status: str
    processing_error: Optional[str] = None
    created_at: str
    updated_at: str

class DocumentChunkModel(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    page_number: int
    text: str
    metadata: Optional[Dict[str, Any]] = None

class DocumentDetailResponse(DocumentResponse):
    chunks_count: int
    sample_chunks: List[DocumentChunkModel] = []

# -----------------
# Dashboard Models
# -----------------
class DashboardStatsResponse(BaseModel):
    total_documents: int
    indexed_documents: int
    total_sessions: int
    total_reports: int
    total_chunks: int
    recent_documents: List[DocumentResponse]
    recent_sessions: List[Dict[str, Any]]

# -----------------
# Citation & RAG Models
# -----------------
class CitationItem(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    page_number: int
    excerpt: str
    score: float
    rank: Optional[int] = None

class ChatMessageCreate(BaseModel):
    content: str
    selected_document_ids: List[str]

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    citations: List[CitationItem] = []
    created_at: str

class ResearchSessionCreate(BaseModel):
    title: Optional[str] = "New Research Session"

class ResearchSessionResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0

# -----------------
# Comparison Models
# -----------------
class ComparisonRequest(BaseModel):
    document_ids: List[str]
    comparison_question: str

class ComparisonItem(BaseModel):
    topic: str
    document_a_evidence: str
    document_b_evidence: str
    relationship: str  # "Agreement", "Difference", "Potential Contradiction", "Insufficient Evidence"
    citations: List[CitationItem] = []
    explanation: str
    human_review_recommended: bool = False

class ComparisonResponse(BaseModel):
    question: str
    documents_compared: List[Dict[str, Any]]
    comparisons: List[ComparisonItem]
    summary: str

# -----------------
# Research Reports
# -----------------
class ReportGenerateRequest(BaseModel):
    research_question: str
    purpose: str = "Executive Decision Making"
    selected_document_ids: List[str]
    title: Optional[str] = None

class ReportSaveRequest(BaseModel):
    title: str
    research_question: str
    purpose: str
    content_markdown: str
    selected_document_ids: List[str]

class ReportUpdateRequest(BaseModel):
    title: Optional[str] = None
    content_markdown: Optional[str] = None

class ReportResponse(BaseModel):
    id: str
    title: str
    research_question: str
    purpose: str
    content_markdown: str
    selected_document_ids: List[str]
    created_at: str
    updated_at: str

# -----------------
# Settings Models
# -----------------
class SettingsResponse(BaseModel):
    groq_api_key_configured: bool
    groq_model: str
    app_host: str
    app_port: int
    max_upload_mb: int
    embedding_model: str
    total_indexed_documents: int
    total_chunks: int

class SettingsUpdateRequest(BaseModel):
    groq_api_key: Optional[str] = None
    groq_model: Optional[str] = None

class TestConnectionResponse(BaseModel):
    success: bool
    message: str
    model: Optional[str] = None

# -----------------
# Evaluation Models
# -----------------
class EvaluationTestCaseResult(BaseModel):
    query: str
    expected_docs: List[str]
    retrieved_docs: List[str]
    hit: bool
    recall: float
    citation_coverage: float
    faithfulness: str

class EvaluationBenchmarkResponse(BaseModel):
    total_queries: int
    hit_rate_at_k: float
    average_recall: float
    average_citation_coverage: float
    results: List[EvaluationTestCaseResult]
    explanation: Dict[str, str]
