from fastapi import APIRouter, Depends

from dependencies import get_current_user
from drink_attributes import SYRUPS, catalog_logging_options
from models import User
from schemas import CatalogResponse

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/drinks", response_model=CatalogResponse)
def list_catalog_drinks(_current_user: User = Depends(get_current_user)):
    return CatalogResponse(
        drinks=catalog_logging_options(),
        syrups=list(SYRUPS),
    )
