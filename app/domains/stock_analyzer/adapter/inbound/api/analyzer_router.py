from fastapi import APIRouter, Depends, HTTPException

from app.domains.stock_analyzer.adapter.outbound.external.openai_analyzer_adapter import OpenAIAnalyzerAdapter
from app.domains.stock_analyzer.adapter.outbound.external.openai_keyword_adapter import OpenAIKeywordAdapter
from app.domains.stock_analyzer.adapter.outbound.external.openai_risk_tag_adapter import OpenAIRiskTagAdapter
from app.domains.stock_analyzer.adapter.outbound.external.openai_sentiment_adapter import OpenAISentimentAdapter
from app.domains.stock_analyzer.adapter.outbound.persistence.article_analysis_repository_impl import InMemoryArticleAnalysisRepository
from app.domains.stock_analyzer.application.request.analyze_article_request import AnalyzeArticleRequest
from app.domains.stock_analyzer.application.response.article_analysis_response import ArticleAnalysisResponse
from app.domains.stock_analyzer.application.response.keyword_extraction_response import KeywordExtractionResponse
from app.domains.stock_analyzer.application.response.risk_tagging_response import RiskTaggingResponse
from app.domains.stock_analyzer.application.response.sentiment_analysis_response import SentimentAnalysisResponse
from app.domains.stock_analyzer.application.usecase.analyze_article_usecase import AnalyzeArticleUseCase
from app.domains.stock_analyzer.application.usecase.analyze_sentiment_usecase import AnalyzeSentimentUseCase
from app.domains.stock_analyzer.application.usecase.extract_keywords_usecase import ExtractKeywordsUseCase
from app.domains.stock_analyzer.application.usecase.generate_risk_tags_usecase import GenerateRiskTagsUseCase
from app.domains.stock_analyzer.application.usecase.get_or_create_analysis_usecase import GetOrCreateAnalysisUseCase
from app.domains.stock_normalizer.adapter.outbound.persistence.repository_registry import normalized_article_repository
from app.infrastructure.config.settings import get_settings

router = APIRouter(prefix="/analyzer", tags=["analyzer"])

_analysis_repository = InMemoryArticleAnalysisRepository()


def _settings():
    return get_settings()


@router.post("/articles", response_model=ArticleAnalysisResponse)
async def analyze_article(request: AnalyzeArticleRequest) -> ArticleAnalysisResponse:
    settings = _settings()
    adapter = OpenAIAnalyzerAdapter(api_key=settings.openai_api_key)
    usecase = AnalyzeArticleUseCase(analyzer_port=adapter)
    return await usecase.execute(request)


@router.get("/articles/{article_id}/keywords", response_model=KeywordExtractionResponse)
async def get_keywords(article_id: str) -> KeywordExtractionResponse:
    settings = _settings()
    usecase = ExtractKeywordsUseCase(
        article_repository=normalized_article_repository,
        keyword_port=OpenAIKeywordAdapter(api_key=settings.openai_api_key),
    )
    try:
        return await usecase.execute(article_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/articles/{article_id}/sentiment", response_model=SentimentAnalysisResponse)
async def get_sentiment(article_id: str) -> SentimentAnalysisResponse:
    settings = _settings()
    usecase = AnalyzeSentimentUseCase(
        article_repository=normalized_article_repository,
        sentiment_port=OpenAISentimentAdapter(api_key=settings.openai_api_key),
    )
    try:
        return await usecase.execute(article_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/articles/{article_id}/risk-tags", response_model=RiskTaggingResponse)
async def get_risk_tags(article_id: str) -> RiskTaggingResponse:
    settings = _settings()
    usecase = GenerateRiskTagsUseCase(
        article_repository=normalized_article_repository,
        risk_tagging_port=OpenAIRiskTagAdapter(api_key=settings.openai_api_key),
    )
    try:
        return await usecase.execute(article_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/articles/{article_id}/analysis", response_model=ArticleAnalysisResponse)
async def get_analysis(article_id: str) -> ArticleAnalysisResponse:
    settings = _settings()
    usecase = GetOrCreateAnalysisUseCase(
        article_repository=normalized_article_repository,
        analysis_repository=_analysis_repository,
        analyzer_port=OpenAIAnalyzerAdapter(api_key=settings.openai_api_key),
    )
    try:
        return await usecase.execute(article_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
