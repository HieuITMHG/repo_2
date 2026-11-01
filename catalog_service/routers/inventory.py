from fastapi import APIRouter
from pydantic import BaseModel
import uuid

# LEVEL 3 (HARD): Router with prefix
router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])

class ReserveRequest(BaseModel):
    sku: str
    quantity: int

@router.post("/reserve")
def reserve_stock(payload: ReserveRequest):
    """
    Full path: POST /api/v1/inventory/reserve
    Matches CatalogClient.reserveInventory() in repo_1.
    """
    reservation_id = f"res_{uuid.uuid4().hex[:8]}"
    return {
        "success": True,
        "sku": payload.sku,
        "reserved_quantity": payload.quantity,
        "reservationId": reservation_id
    }
