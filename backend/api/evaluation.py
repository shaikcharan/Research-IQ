from fastapi import APIRouter, Query
from backend.models import EvaluationBenchmarkResponse, EvaluationTestCaseResult
from backend.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/evaluation", tags=["Evaluation & Benchmark"])

@router.get("/benchmark", response_model=EvaluationBenchmarkResponse)
def run_evaluation_benchmark(top_k: int = Query(5, ge=1, le=20)):
    """
    Run empirical RAG benchmark against indexed documents.
    Computes Hit Rate@K, Recall@K, and Citation Coverage Rate.
    """
    data = EvaluationService.run_benchmark(top_k=top_k)
    results_objs = [
        EvaluationTestCaseResult(
            query=r["query"],
            expected_docs=r["expected_docs"],
            retrieved_docs=r["retrieved_docs"],
            hit=r["hit"],
            recall=r["recall"],
            citation_coverage=r["citation_coverage"],
            faithfulness=r["faithfulness"]
        ) for r in data["results"]
    ]

    return EvaluationBenchmarkResponse(
        total_queries=data["total_queries"],
        hit_rate_at_k=data["hit_rate_at_k"],
        average_recall=data["average_recall"],
        average_citation_coverage=data["average_citation_coverage"],
        results=results_objs,
        explanation=data["explanation"]
    )
