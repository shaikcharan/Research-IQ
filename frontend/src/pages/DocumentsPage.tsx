import React, { useState, useEffect, useRef } from 'react';
import {
  Upload,
  Files,
  Search,
  Trash2,
  RefreshCw,
  Eye,
  FileText,
  AlertTriangle,
  CheckCircle2,
  Layers,
  Sparkles,
  ArrowUpDown
} from 'lucide-react';
import { api } from '../services/api';
import { DocumentItem, DocumentDetail } from '../types';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface DocumentsPageProps {
  onStartResearch: (docIds: string[]) => void;
}

export const DocumentsPage: React.FC<DocumentsPageProps> = ({ onStartResearch }) => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [order, setOrder] = useState('desc');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Detail Modal
  const [detailDoc, setDetailDoc] = useState<DocumentDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  // Delete Confirmation Modal
  const [docToDelete, setDocToDelete] = useState<DocumentItem | null>(null);
  const [deleting, setDeleting] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchDocs = async () => {
    try {
      setLoading(true);
      const data = await api.getDocuments({
        search: search || undefined,
        status: statusFilter || undefined,
        sort_by: sortBy,
        order: order,
      });
      setDocuments(data);
      setErrorMsg(null);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to fetch documents.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, [search, statusFilter, sortBy, order]);

  const handleFileUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const fileArray = Array.from(files);
    setUploading(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const uploaded = await api.uploadDocuments(fileArray);
      setSuccessMsg(`Successfully uploaded and indexed ${uploaded.length} document(s).`);
      await fetchDocs();
    } catch (err: any) {
      setErrorMsg(err.message || 'File upload failed.');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files) {
      handleFileUpload(e.dataTransfer.files);
    }
  };

  const handleViewDetail = async (docId: string) => {
    try {
      setDetailLoading(true);
      const detail = await api.getDocumentDetail(docId);
      setDetailDoc(detail);
    } catch (err: any) {
      alert(`Could not load document details: ${err.message}`);
    } finally {
      setDetailLoading(false);
    }
  };

  const handleConfirmDelete = async () => {
    if (!docToDelete) return;
    try {
      setDeleting(true);
      await api.deleteDocument(docToDelete.id);
      setSelectedIds((prev) => prev.filter((id) => id !== docToDelete.id));
      setDocToDelete(null);
      await fetchDocs();
    } catch (err: any) {
      alert(`Delete failed: ${err.message}`);
    } finally {
      setDeleting(false);
    }
  };

  const handleReprocess = async (docId: string) => {
    try {
      await api.reprocessDocument(docId);
      await fetchDocs();
    } catch (err: any) {
      alert(`Reprocessing failed: ${err.message}`);
    }
  };

  const toggleSelectDoc = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === documents.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(documents.map((d) => d.id));
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Document Management Library
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Upload PDFs for automatic page-level text extraction, overlapping chunking, and FAISS vector indexing.
          </p>
        </div>

        {selectedIds.length > 0 && (
          <button
            onClick={() => onStartResearch(selectedIds)}
            className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition"
          >
            <Sparkles className="w-4 h-4" />
            <span>Research {selectedIds.length} Selected Paper{selectedIds.length === 1 ? '' : 's'}</span>
          </button>
        )}
      </div>

      {/* Upload Dropzone */}
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-3xl p-8 text-center transition-all bg-white dark:bg-slate-900 ${
          uploading
            ? 'border-indigo-400 bg-indigo-50/50 dark:bg-indigo-950/20'
            : 'border-slate-300 dark:border-slate-700 hover:border-indigo-400'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          multiple
          accept=".pdf"
          onChange={(e) => handleFileUpload(e.target.files)}
          className="hidden"
        />

        <div className="max-w-md mx-auto space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mx-auto shadow-sm">
            <Upload className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-800 dark:text-slate-100">
              Drag & Drop your PDF research papers here
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Supports multiple PDFs up to 20MB each. Page numbers and metadata are preserved for citations.
            </p>
          </div>
          <button
            type="button"
            disabled={uploading}
            onClick={() => fileInputRef.current?.click()}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 transition shadow-sm"
          >
            {uploading ? 'Extracting & Indexing...' : 'Browse PDF Files'}
          </button>
        </div>
      </div>

      {/* Notifications */}
      {errorMsg && (
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-xl text-xs text-rose-700 dark:text-rose-400 flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {successMsg && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-xl text-xs text-emerald-700 dark:text-emerald-400 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Search, Filter, Sort Controls */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by title or filename..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          {/* Status filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 text-xs rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 focus:outline-none"
          >
            <option value="">All Statuses</option>
            <option value="Ready">Ready</option>
            <option value="Indexing">Indexing</option>
            <option value="Extracting">Extracting</option>
            <option value="Failed">Failed</option>
          </select>

          {/* Sort field */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 text-xs rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 focus:outline-none"
          >
            <option value="created_at">Date Uploaded</option>
            <option value="title">Title</option>
            <option value="file_size">File Size</option>
            <option value="page_count">Page Count</option>
          </select>

          {/* Sort order */}
          <button
            onClick={() => setOrder(order === 'asc' ? 'desc' : 'asc')}
            title="Toggle sort direction"
            className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
          >
            <ArrowUpDown className="w-4 h-4" />
          </button>

          {/* Refresh */}
          <button
            onClick={fetchDocs}
            title="Refresh list"
            className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Documents Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-800/40 text-slate-400 font-semibold">
                <th className="p-4 w-10">
                  <input
                    type="checkbox"
                    checked={documents.length > 0 && selectedIds.length === documents.length}
                    onChange={toggleSelectAll}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                  />
                </th>
                <th className="p-4">Document Title & Filename</th>
                <th className="p-4">Pages</th>
                <th className="p-4">Size</th>
                <th className="p-4">Status</th>
                <th className="p-4">Uploaded</th>
                <th className="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {documents.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-400">
                    No documents found. Upload PDF files above to begin.
                  </td>
                </tr>
              ) : (
                documents.map((doc) => {
                  const isChecked = selectedIds.includes(doc.id);
                  return (
                    <tr
                      key={doc.id}
                      className={`hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition ${
                        isChecked ? 'bg-indigo-50/30 dark:bg-indigo-950/20' : ''
                      }`}
                    >
                      <td className="p-4">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => toggleSelectDoc(doc.id)}
                          className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                        />
                      </td>
                      <td className="p-4 max-w-xs">
                        <p className="font-semibold text-slate-900 dark:text-white truncate">
                          {doc.title}
                        </p>
                        <p className="text-[11px] text-slate-400 truncate mt-0.5">
                          {doc.filename}
                        </p>
                      </td>
                      <td className="p-4 text-slate-600 dark:text-slate-300">
                        {doc.page_count} pgs
                      </td>
                      <td className="p-4 text-slate-600 dark:text-slate-300">
                        {(doc.file_size / 1024).toFixed(1)} KB
                      </td>
                      <td className="p-4">
                        <Badge
                          variant={doc.processing_status === 'Ready' ? 'ready' : doc.processing_status === 'Failed' ? 'failed' : 'indexing'}
                        >
                          {doc.processing_status}
                        </Badge>
                      </td>
                      <td className="p-4 text-slate-400">
                        {new Date(doc.created_at).toLocaleDateString()}
                      </td>
                      <td className="p-4 text-right space-x-2">
                        <button
                          onClick={() => handleViewDetail(doc.id)}
                          title="Inspect chunks and metadata"
                          className="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        {doc.processing_status === 'Failed' && (
                          <button
                            onClick={() => handleReprocess(doc.id)}
                            title="Retry extraction & indexing"
                            className="p-1.5 rounded-lg text-amber-500 hover:text-amber-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
                          >
                            <RefreshCw className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={() => setDocToDelete(doc)}
                          title="Delete document and remove from FAISS index"
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Document Detail Modal */}
      <Modal
        isOpen={!!detailDoc}
        onClose={() => setDetailDoc(null)}
        title={detailDoc?.title || 'Document Details'}
        maxWidth="2xl"
      >
        {detailDoc && (
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-3 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
              <div>
                <span className="text-slate-400">Filename:</span>
                <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{detailDoc.filename}</p>
              </div>
              <div>
                <span className="text-slate-400">Total Extracted Chunks:</span>
                <p className="font-semibold text-indigo-600 dark:text-indigo-400 mt-0.5">{detailDoc.chunks_count} chunks</p>
              </div>
              <div>
                <span className="text-slate-400">Pages:</span>
                <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{detailDoc.page_count}</p>
              </div>
              <div>
                <span className="text-slate-400">Processing Status:</span>
                <p className="font-semibold mt-0.5">{detailDoc.processing_status}</p>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-slate-800 dark:text-slate-100 mb-2">
                Sample Extracted Chunks with Page Citations (First {detailDoc.sample_chunks.length}):
              </h4>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {detailDoc.sample_chunks.map((chk, i) => (
                  <div
                    key={chk.id}
                    className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"
                  >
                    <div className="flex items-center justify-between mb-1 text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">
                      <span>Chunk #{chk.chunk_index + 1}</span>
                      <span>Page {chk.page_number}</span>
                    </div>
                    <p className="text-slate-600 dark:text-slate-300 leading-relaxed italic">
                      "{chk.text}"
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={!!docToDelete}
        onClose={() => setDocToDelete(null)}
        title="Delete Document"
        maxWidth="md"
      >
        {docToDelete && (
          <div className="space-y-4 text-xs">
            <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
              Are you sure you want to delete <strong className="text-slate-900 dark:text-white">{docToDelete.title}</strong>?
              This will remove the file from storage, cascade-delete all chunks in SQLite, and safely rebuild the FAISS vector index.
            </p>
            <div className="flex justify-end space-x-3 pt-2">
              <button
                onClick={() => setDocToDelete(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                disabled={deleting}
                className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-semibold transition"
              >
                {deleting ? 'Deleting & Reindexing...' : 'Confirm Delete'}
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};
