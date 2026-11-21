from fastapi import APIRouter, HTTPException
from backend.models import ComparisonRequest, ComparisonResponse, ComparisonItem, CitationItem
from backend.services.comparison_service import ComparisonService

router = APIRouter(prefix="/research", tags=["Comparison & Contradictions"])

@router.post("/compare", response_model=ComparisonResponse)
async def compare_documents_endpoint(data: ComparisonRequest):
    """
    Compare findings across two or more documents and detect potential contradictions.
    """
    if len(data.document_ids) < 2:
        raise HTTPException(
            status_code=400,
            detail="Comparative analysis requires at least two selected documents."
        )

    if not data.comparison_question.strip():
        raise HTTPException(
            status_code=400,
            detail="Comparison question cannot be empty."
        )

    try:
        result = await ComparisonService.compare_documents(
            document_ids=data.document_ids,
            question=data.comparison_question.strip()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    comparisons_objs = []
    for comp in result.get("comparisons", []):
        cits = [CitationItem(**c) for c in comp.get("citations", [])]
        comparisons_objs.append(ComparisonItem(
            topic=comp.get("topic", "Comparative Finding"),
            document_a_evidence=comp.get("document_a_evidence", ""),
            document_b_evidence=comp.get("document_b_evidence", ""),
            relationship=comp.get("relationship", "Difference"),
            citations=cits,
            explanation=comp.get("explanation", ""),
            human_review_recommended=comp.get("human_review_recommended", False)
        ))

    return ComparisonResponse(
        question=result.get("question", data.comparison_question),
        documents_compared=result.get("documents_compared", []),
        comparisons=comparisons_objs,
        summary=result.get("summary", "")
    )
