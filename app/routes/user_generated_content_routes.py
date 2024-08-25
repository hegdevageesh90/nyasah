from typing import List

from fastapi import APIRouter, HTTPException

from app.models.user_generated_content import UserGeneratedContent
from app.services.user_generated_content_service import (
    add_user_generated_content,
    get_content_by_user,
    get_content_by_type,
    update_ugc,
    get_content_by_content_id
)

router = APIRouter()


@router.post("/ugc", response_model=UserGeneratedContent, status_code=201)
def create_user_generated_content(content: UserGeneratedContent):
    try:
        saved_content = add_user_generated_content(content)
        return saved_content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ugc/{content_id}", response_model=UserGeneratedContent)
def update_ugc_route(content_id: str, data: UserGeneratedContent):
    try:
        result = update_ugc(content_id, data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ugc/{content_id}", response_model=UserGeneratedContent)
def get_content_by_content_id_route(content_id: str):
    try:
        content = get_content_by_content_id(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ugc/user/{user_id}", response_model=List[UserGeneratedContent])
def get_content_by_user_route(user_id: str):
    try:
        content_list = get_content_by_user(user_id)
        return content_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ugc/type/{content_type}", response_model=List[UserGeneratedContent])
def get_content_by_type_route(content_type: str):
    try:
        content_list = get_content_by_type(content_type)
        return content_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
