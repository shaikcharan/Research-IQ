import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.environ['MPLCONFIGDIR'] = os.path.join(os.path.dirname(__file__), '..', '.mpl_cache')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ResearchIQ_Internship_Report', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper function to create clean engineering architecture boxes
def draw_box(ax, x, y, w, h, title, subtitle="", color="#1E293B", bg_color="#FFFFFF", border_color="#0F172A", lw=1.5):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw)
    ax.add_patch(rect)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=color, family="sans-serif")
        ax.text(x + w/2, y + h*0.32, subtitle, ha="center", va="center", fontsize=8, color="#475569", family="sans-serif")
    else:
        ax.text(x + w/2, y + h/2, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=color, family="sans-serif")

def draw_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=1.4, mutation_scale=14))
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.02, label, ha="center", va="bottom", fontsize=7.5, color="#334155", fontweight="semibold")

# 1. Figure 6.1: Overall System Architecture
def make_fig_6_1():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    # Layer 1: Client
    draw_box(ax, 0.4, 5.2, 9.2, 0.9, "PRESENTATION LAYER (FRONTEND)", "React 19 | TypeScript | Vite | Tailwind CSS | Lucide Icons | 3-Panel Workspace UI", bg_color="#F8FAFC", border_color="#3B82F6")
    
    # Layer 2: API Gateway
    draw_box(ax, 0.4, 3.8, 9.2, 0.9, "APPLICATION & API GATEWAY LAYER (FASTAPI)", "FastAPI 0.110+ | Uvicorn ASGI Server | Pydantic v2 Models | REST Endpoints (/api/*)", bg_color="#F8FAFC", border_color="#10B981")

    # Layer 3: Services Sub-Modules
    draw_box(ax, 0.4, 2.0, 2.1, 1.3, "Ingestion & Extraction", "PyMuPDF (fitz)\nSHA-256 Duplication Check\nPage-Level Metadata", bg_color="#FFFFFF")
    draw_box(ax, 2.7, 2.0, 2.1, 1.3, "Text Chunking", "Sentence Boundary Splitting\n750 Char Size | 150 Overlap\nPreserves Page Index", bg_color="#FFFFFF")
    draw_box(ax, 5.0, 2.0, 2.1, 1.3, "Vectorization & Index", "all-MiniLM-L6-v2 (384-dim)\nFAISS IndexFlatIP\nSQLite FTS5 BM25", bg_color="#FFFFFF")
    draw_box(ax, 7.3, 2.0, 2.3, 1.3, "RAG & Reasoning", "Reciprocal Rank Fusion\nGroq Cloud Llama-3.3-70b\nContradiction Engine", bg_color="#FFFFFF")

    # Layer 4: Storage
    draw_box(ax, 0.4, 0.3, 9.2, 1.1, "PERSISTENCE & STORAGE LAYER", "SQLite DB (Documents, Chunks, Sessions, Reports) | FAISS Binaries | File Uploads & PDF Exports", bg_color="#F8FAFC", border_color="#6366F1")

    # Connections
    draw_arrow(ax, 5.0, 5.2, 5.0, 4.7, "HTTP / JSON API Requests")
    draw_arrow(ax, 1.45, 3.8, 1.45, 3.3)
    draw_arrow(ax, 3.75, 3.8, 3.75, 3.3)
    draw_arrow(ax, 6.05, 3.8, 6.05, 3.3)
    draw_arrow(ax, 8.45, 3.8, 8.45, 3.3)

    draw_arrow(ax, 2.5, 2.65, 2.7, 2.65)
    draw_arrow(ax, 4.8, 2.65, 5.0, 2.65)
    draw_arrow(ax, 7.1, 2.65, 7.3, 2.65)

    draw_arrow(ax, 1.45, 2.0, 1.45, 1.4)
    draw_arrow(ax, 6.05, 2.0, 6.05, 1.4)
    draw_arrow(ax, 8.45, 2.0, 8.45, 1.4)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_1_architecture.png"), dpi=300)
    plt.close()

# 2. Figure 6.2: Document Processing Workflow
def make_fig_6_2():
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    draw_box(ax, 0.3, 1.3, 1.6, 1.2, "1. PDF Upload", "Multi-file drop\nMax 20 MB/file", bg_color="#F8FAFC")
    draw_box(ax, 2.2, 1.3, 1.6, 1.2, "2. SHA-256 Hash", "Duplicate check\nStore file locally", bg_color="#F8FAFC")
    draw_box(ax, 4.1, 1.3, 1.7, 1.2, "3. PyMuPDF Parse", "Extract page text\n1-indexed pages", bg_color="#F8FAFC")
    draw_box(ax, 6.1, 1.3, 1.7, 1.2, "4. Text Validity", "Check >= 50 chars\nReject image-only", bg_color="#F8FAFC")
    draw_box(ax, 8.1, 1.3, 1.6, 1.2, "5. DB Registration", "Insert metadata\nStatus = Extracting", bg_color="#F8FAFC")

    draw_arrow(ax, 1.9, 1.9, 2.2, 1.9)
    draw_arrow(ax, 3.8, 1.9, 4.1, 1.9)
    draw_arrow(ax, 5.8, 1.9, 6.1, 1.9)
    draw_arrow(ax, 7.8, 1.9, 8.1, 1.9)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_2_doc_processing.png"), dpi=300)
    plt.close()

# 3. Figure 6.3: Chunking & Embedding Workflow
def make_fig_6_3():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    draw_box(ax, 0.3, 1.5, 1.7, 1.2, "Raw Page Text", "Page Number\nDocument Title", bg_color="#F8FAFC")
    draw_box(ax, 2.3, 1.5, 1.8, 1.2, "Sentence Chunker", "Regex Splitter\n750 char window\n150 char overlap", bg_color="#F8FAFC")
    draw_box(ax, 4.4, 1.5, 1.7, 1.2, "Chunk Schema", "doc_id, page_no\nchunk_id, text", bg_color="#F8FAFC")
    draw_box(ax, 6.4, 1.5, 1.7, 1.2, "all-MiniLM-L6-v2", "SentenceTransformers\n384 Dimensions", bg_color="#F8FAFC")
    draw_box(ax, 8.4, 1.5, 1.3, 1.2, "FAISS Index", "IndexFlatIP\nL2 Normalization", bg_color="#F8FAFC")

    draw_arrow(ax, 2.0, 2.1, 2.3, 2.1)
    draw_arrow(ax, 4.1, 2.1, 4.4, 2.1)
    draw_arrow(ax, 6.1, 2.1, 6.4, 2.1)
    draw_arrow(ax, 8.1, 2.1, 8.4, 2.1)

    # SQLite FTS5 branch
    draw_box(ax, 6.4, 0.1, 3.3, 0.9, "SQLite FTS5 Full-Text Search Table", "Keyword Indexing using Porter Tokenizer", bg_color="#EFF6FF", border_color="#3B82F6")
    draw_arrow(ax, 5.25, 1.5, 5.25, 0.55)
    draw_arrow(ax, 5.25, 0.55, 6.4, 0.55)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_3_chunking_embedding.png"), dpi=300)
    plt.close()

# 4. Figure 6.4: FAISS Vector Indexing Architecture
def make_fig_6_4():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    draw_box(ax, 0.4, 2.7, 2.6, 1.3, "Document Chunks Pool", "SQLite Table: document_chunks\nID, DocID, PageNo, Text", bg_color="#F8FAFC")
    draw_box(ax, 3.6, 2.7, 2.8, 1.3, "Embedding Engine", "SentenceTransformers Encoder\nBatch Processing (batch_size=32)\nL2 Unit Length Normalization", bg_color="#F8FAFC")
    draw_box(ax, 7.0, 2.7, 2.6, 1.3, "FAISS Vector Index", "IndexFlatIP (Inner Product)\n384 Dimensions\nExact Cosine Similarity", bg_color="#F8FAFC", border_color="#10B981")

    draw_arrow(ax, 3.0, 3.35, 3.6, 3.35, "Text Batches")
    draw_arrow(ax, 6.4, 3.35, 7.0, 3.35, "Normalized Floats")

    # Disk storage and mappings
    draw_box(ax, 3.6, 0.5, 2.8, 1.3, "Chunk ID Map Storage", "JSON Mapping Array:\n[chunk_id_0, chunk_id_1, ...]\nchunk_id_map.json", bg_color="#FFFBEB", border_color="#D97706")
    draw_box(ax, 7.0, 0.5, 2.6, 1.3, "Binary Index File", "faiss_index.bin\nLocal Persistent Storage\nAtomic Rebuild Capability", bg_color="#FFFBEB", border_color="#D97706")

    draw_arrow(ax, 5.0, 2.7, 5.0, 1.8, "Synchronize IDs")
    draw_arrow(ax, 8.3, 2.7, 8.3, 1.8, "Save / Load")

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_4_faiss_indexing.png"), dpi=300)
    plt.close()

# 5. Figure 6.5: Retrieval-Augmented Generation Architecture
def make_fig_6_5():
    fig, ax = plt.subplots(figsize=(10, 5.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    draw_box(ax, 0.4, 3.3, 2.2, 1.2, "User Query", "User Question\nSelected Document IDs", bg_color="#F8FAFC")
    draw_box(ax, 3.2, 3.8, 2.2, 0.9, "FAISS Dense Search", "Cosine Similarity Top-15", bg_color="#FFFFFF")
    draw_box(ax, 3.2, 2.6, 2.2, 0.9, "SQLite FTS5 BM25", "Keyword Matches Top-15", bg_color="#FFFFFF")

    draw_box(ax, 5.9, 3.0, 2.0, 1.5, "Reciprocal Rank Fusion", "RRF (k=60)\nRRF(d)=∑1/(60+r)\nDocument Filter", bg_color="#F8FAFC", border_color="#6366F1")
    draw_box(ax, 8.3, 3.0, 1.4, 1.5, "Top-K Chunks", "Top 6 Evidence\nOriginal Pages\nTitle Metadata", bg_color="#F8FAFC")

    draw_box(ax, 3.2, 0.5, 6.5, 1.5, "Evidence-Grounded LLM Synthesis (Groq Cloud API)", "Model: llama-3.3-70b-versatile | Strict Grounding System Instruction\nOutput: Synthesized Answer + Clickable Evidence Citations [Title, p. X]", bg_color="#F0FDF4", border_color="#16A34A")

    draw_arrow(ax, 2.6, 4.0, 3.2, 4.15)
    draw_arrow(ax, 2.6, 3.6, 3.2, 3.15)
    draw_arrow(ax, 5.4, 4.15, 5.9, 3.9)
    draw_arrow(ax, 5.4, 3.15, 5.9, 3.4)
    draw_arrow(ax, 7.9, 3.75, 8.3, 3.75)
    draw_arrow(ax, 9.0, 3.0, 9.0, 2.0)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_5_rag_architecture.png"), dpi=300)
    plt.close()

# 6. Figure 6.6: Complete System Workflow
def make_fig_6_6():
    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.0)
    ax.axis("off")

    draw_box(ax, 0.5, 4.6, 2.6, 1.0, "1. Ingestion Phase", "Upload PDFs -> PyMuPDF Page Parse -> SQLite Chunks & FTS5 -> FAISS Embeddings", bg_color="#F8FAFC")
    draw_box(ax, 3.7, 4.6, 2.6, 1.0, "2. Selection Phase", "User checks target documents in Sources Panel (Multi-Doc Isolation)", bg_color="#F8FAFC")
    draw_box(ax, 6.9, 4.6, 2.6, 1.0, "3. Query Phase", "Natural language inquiry entered in Research Workspace", bg_color="#F8FAFC")

    draw_arrow(ax, 3.1, 5.1, 3.7, 5.1)
    draw_arrow(ax, 6.3, 5.1, 6.9, 5.1)
    draw_arrow(ax, 8.2, 4.6, 8.2, 3.8)

    draw_box(ax, 6.9, 2.8, 2.6, 1.0, "4. Hybrid Retrieval", "FAISS Cosine + SQLite FTS5 BM25 combined via Reciprocal Rank Fusion", bg_color="#EFF6FF", border_color="#3B82F6")
    draw_box(ax, 3.7, 2.8, 2.6, 1.0, "5. Evidence Assembly", "Filter chunks by selectedDocIds, verify threshold, assemble context", bg_color="#EFF6FF", border_color="#3B82F6")
    draw_box(ax, 0.5, 2.8, 2.6, 1.0, "6. Grounded Generation", "Groq Llama-3.3-70b synthesizes response strictly citing [Doc, p. X]", bg_color="#EFF6FF", border_color="#3B82F6")

    draw_arrow(ax, 6.9, 3.3, 6.3, 3.3)
    draw_arrow(ax, 3.7, 3.3, 3.1, 3.3)
    draw_arrow(ax, 1.8, 2.8, 1.8, 2.0)

    draw_box(ax, 0.5, 0.6, 4.2, 1.4, "7A. Research Workspace Output", "• Markdown Grounded Answer\n• Clickable Citation Badges\n• Interactive Evidence Explorer Panel", bg_color="#F0FDF4", border_color="#16A34A")
    draw_box(ax, 5.3, 0.6, 4.2, 1.4, "7B. Intelligence Reports & Analysis", "• Multi-Doc Contradiction Matrix\n• 13-Section Academic Brief Synthesis\n• 1-Click Export to Markdown & PDF", bg_color="#F0FDF4", border_color="#16A34A")

    draw_arrow(ax, 1.8, 2.0, 2.5, 2.0)
    draw_arrow(ax, 2.5, 2.0, 2.5, 2.0)
    draw_arrow(ax, 1.8, 2.0, 1.8, 2.0)
    draw_arrow(ax, 4.7, 2.8, 7.4, 2.0)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_6_6_complete_workflow.png"), dpi=300)
    plt.close()

# Generate Testing Screenshot Placeholders (Figures 9.1 to 9.12)
def make_test_placeholder(fig_num, test_title, filename):
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300) # 16:9 approx
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Light grey thin border, white background
    rect = patches.Rectangle((0.1, 0.1), 15.8, 8.8, facecolor="#FAFAFA", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(rect)

    # Inner dotted border
    inner = patches.Rectangle((0.6, 0.6), 14.8, 7.8, facecolor="#FFFFFF", edgecolor="#E2E8F0", linestyle="--", linewidth=1.5)
    ax.add_patch(inner)

    # Icon / badge placeholder
    badge = patches.FancyBboxPatch((6.0, 5.4), 4.0, 1.2, boxstyle="round,pad=0.08,rounding_size=0.15", facecolor="#EEF2FF", edgecolor="#6366F1", linewidth=1.5)
    ax.add_patch(badge)
    ax.text(8.0, 6.0, f"FIGURE {fig_num}", ha="center", va="center", fontsize=12, fontweight="bold", color="#4338CA", family="sans-serif")

    # Centered Title & Placeholder Instruction
    ax.text(8.0, 4.2, test_title, ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A", family="sans-serif")
    ax.text(8.0, 3.2, "[ INSERT ACTUAL APPLICATION SCREENSHOT HERE ]", ha="center", va="center", fontsize=12, fontweight="bold", color="#64748B", family="sans-serif")
    ax.text(8.0, 2.2, "Capture running ResearchIQ interface at http://127.0.0.1:8000\nPaste full resolution screenshot over this placeholder frame", ha="center", va="center", fontsize=9.5, color="#94A3B8", family="sans-serif")

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300)
    plt.close()

print("Generating architecture diagrams...")
make_fig_6_1()
make_fig_6_2()
make_fig_6_3()
make_fig_6_4()
make_fig_6_5()
make_fig_6_6()

test_cases = [
    ("9.1", "TC-01: Application Launch & Dashboard Interface", "fig_9_1_app_launch.png"),
    ("9.2", "TC-02 & TC-03: Drag-and-Drop PDF Upload & Document Library", "fig_9_2_pdf_upload.png"),
    ("9.3", "TC-05: PDF Text & Page Number Extraction Output", "fig_9_3_text_extraction.png"),
    ("9.4", "TC-06: Text Cleaning and Preprocessing Validation", "fig_9_4_text_preprocessing.png"),
    ("9.5", "TC-07: Sentence-Aware Overlapping Text Chunking Output", "fig_9_5_chunking.png"),
    ("9.6", "TC-08: SentenceTransformers Embedding Generation (384-dim)", "fig_9_6_embeddings.png"),
    ("9.7", "TC-09: FAISS Vector Indexing & ID Mapping Persistence", "fig_9_7_faiss_indexing.png"),
    ("9.8", "TC-10 & TC-11: Hybrid Semantic & Keyword Document Retrieval", "fig_9_8_semantic_retrieval.png"),
    ("9.9", "TC-12: RAG Grounded Question Answering & Citation Tags", "fig_9_9_rag_chat.png"),
    ("9.10", "TC-13: Multi-Document Claim Comparison & Contradiction Matrix", "fig_9_10_comparison.png"),
    ("9.11", "TC-14: Evidence Explorer Interactive Chunk Verification", "fig_9_11_evidence_explorer.png"),
    ("9.12", "TC-15: Final 13-Section Executive Brief PDF & Markdown Export", "fig_9_12_report_export.png")
]

print("Generating test placeholders...")
for num, title, fname in test_cases:
    make_test_placeholder(num, title, fname)

print("All diagrams and test placeholders generated successfully!")
