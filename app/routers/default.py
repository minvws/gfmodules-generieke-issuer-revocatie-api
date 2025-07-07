import logging
from pathlib import Path

from fastapi import APIRouter, Response
from starlette.requests import Request

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/version.json")
def version_json(_request: Request) -> Response:
    try:
        with open(Path(__file__).parent.parent.parent / "version.json", "r") as file:
            content = file.read()
    except BaseException as e:
        logger.info("Version info could not be loaded: %s" % e)
        return Response(status_code=404)

    return Response(content)
