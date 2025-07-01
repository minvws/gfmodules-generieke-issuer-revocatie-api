import logging

from fastapi import APIRouter, Depends, Response

from app.container import get_allocation_service
from app.services.allocation_service import AllocationService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/allocate")
def allocate(allocation_service: AllocationService = Depends(get_allocation_service)) -> Response:
    """
    Allocate a new index using the allocation service.
    """

    logger.info("Allocating a new index")

    try:
        idx = allocation_service.allocate()
    except Exception as e:
        logger.error(f"Error allocating index: {e}")
        return Response(status_code=500, content=str(e))

    return Response(content=str(idx), media_type="application/json")
