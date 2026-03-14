from fastapi import APIRouter, Depends, HTTPException

from app.domains.stock_normalizer.adapter.outbound.persistence.normalized_disclosure_repository_impl import InMemoryNormalizedDisclosureRepository
from app.domains.stock_normalizer.application.request.normalize_disclosure_request import NormalizeDisclosureRequest
from app.domains.stock_normalizer.application.response.normalize_disclosure_response import NormalizeDisclosureResponse
from app.domains.stock_normalizer.application.usecase.normalize_disclosure_usecase import NormalizeDisclosureUseCase
from app.domains.stock_normalizer.application.usecase.normalized_disclosure_repository_port import NormalizedDisclosureRepositoryPort

router = APIRouter(prefix="/normalizer/disclosures", tags=["stock_normalizer"])


def get_repository() -> NormalizedDisclosureRepositoryPort:
    return InMemoryNormalizedDisclosureRepository()


@router.post("", response_model=NormalizeDisclosureResponse, status_code=201)
async def normalize_disclosure(
    request: NormalizeDisclosureRequest,
    repository: NormalizedDisclosureRepositoryPort = Depends(get_repository),
):
    try:
        usecase = NormalizeDisclosureUseCase(repository)
        return await usecase.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
