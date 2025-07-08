import logging
from typing import Optional

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from app.container import get_revocation_service
from app.services.revokation_service import RevocationService

logger = logging.getLogger(__name__)
router = APIRouter()


class RevokeRequest(BaseModel):
    index: int
    reason: Optional[str] = None


class UnrevokeRequest(BaseModel):
    index: int


@router.post("/revoke")
def revoke(request: RevokeRequest, revocation_service: RevocationService = Depends(get_revocation_service)) -> Response:
    """
    Revoke a credential by its index.
    """
    logger.info(f"Revoking version with index: {request.index}, reason: {request.reason}")

    try:
        revocation_service.revoke(request.index, request.reason)
        return Response(status_code=204)
    except Exception as e:
        logger.error(f"Error revoking version: {e}")
        return Response(status_code=400, content=str(e))


@router.post("/unrevoke")
def unrevoke(
    request: UnrevokeRequest, revocation_service: RevocationService = Depends(get_revocation_service)
) -> Response:
    """
    Unrevoke a credential by its index.
    """
    logger.info(f"Unrevoking version with index: {request.index}")

    try:
        revocation_service.unrevoke(request.index)
        return Response(status_code=204)
    except Exception as e:
        logger.error(f"Error unrevoking version: {e}")
        return Response(status_code=400, content=str(e))
