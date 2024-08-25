from typing import List

from fastapi import APIRouter, HTTPException

from app.models.review import Review
from app.services.review_service import add_review, get_reviews_by_product

router = APIRouter()


@router.post("/reviews", response_model=Review, status_code=201)
def create_review(review: Review):
    try:
        saved_review = add_review(review)
        return saved_review
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reviews/{product_id}", response_model=List[Review])
def list_reviews(product_id: str):
    try:
        reviews = get_reviews_by_product(product_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
