import logging
from typing import Optional

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from app.container import get_credential_generator
from app.services.credential_generator import VerifiableCredentialGenerator

logger = logging.getLogger(__name__)
router = APIRouter()


class RevokeRequest(BaseModel):
    index: int
    reason: Optional[str] = None


@router.get("/")
def bitstring(credential_generator: VerifiableCredentialGenerator = Depends(get_credential_generator)) -> Response:
    token = credential_generator.generate()
    return Response(token, status_code=200)
