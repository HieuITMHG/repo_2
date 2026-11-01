from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from .routers.inventory import router as inventory_router

app = FastAPI(title="Repo 2 - Catalog Service", version="2.0.0")

# Mount sub-router
app.include_router(inventory_router)

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float

SAMPLE_PRODUCTS = {
    "prod_001": ProductResponse(id="prod_001", name="Wireless Mechanical Keyboard", price=129.99),
    "prod_002": ProductResponse(id="prod_002", name="Ergonomic Mouse", price=69.50)
}

@app.get("/api/v1/health")
def catalog_health():
    """Matches repo_1 checkCatalogHealth()"""
    return {"status": "ok", "service": "catalog_service"}

@app.get("/api/v1/products", response_model=List[ProductResponse])
def list_products():
    """
    LEVEL 1 (EASY): Exact static path match.
    Matches repo_1 CatalogClient.listProducts()
    """
    return list(SAMPLE_PRODUCTS.values())

@app.get("/api/v1/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: str):
    """
    LEVEL 2 (MEDIUM): Path parameter template matching.
    Matches repo_1 CatalogClient.getProductDetails(productId)
    """
    if product_id not in SAMPLE_PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    return SAMPLE_PRODUCTS[product_id]

@app.get("/api/v1/internal/health")
def internal_health():
    """
    LEVEL 3 (CALLER-LOCAL FLOOR TEST):
    Duplicate route name with repo_1.
    """
    return {"service": "repo_2_catalog_service", "status": "healthy"}
