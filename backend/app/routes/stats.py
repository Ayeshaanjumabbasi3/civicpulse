from fastapi import APIRouter, Request, Response

from app.schemas.stats import StatsResponse

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
def stats(request: Request, response: Response):
    data, cache_status = request.app.state.stats_service.get()
    response.headers["X-Cache"] = cache_status
    return data
