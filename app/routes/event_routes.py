from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.models.event import Event
from app.services.record_event_service import RecordEventService
from app.services.notification_service import NotificationService
from app.utils.redis_utils import RedisUtils

router = APIRouter()


def get_record_event_service() -> RecordEventService:
    redis_utils = RedisUtils()
    return RecordEventService(redis_utils)


def get_notification_service() -> NotificationService:
    redis_utils = RedisUtils()
    return NotificationService(redis_utils)


@router.post("/record/view")
def record_view(event: Event, service: RecordEventService = Depends(get_record_event_service)):
    try:
        return service.record_view(event.tenant_id, event.product_id, event.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/record/purchase")
def record_purchase(event: Event, service: RecordEventService = Depends(get_record_event_service)):
    try:
        return service.record_purchase(event.tenant_id, event.product_id, event.user_id, event.location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notify/view")
def get_view_notification(
    tenant_id: str,
    product_id: str,
    start_time: Optional[str] = Query(None, description="Start time for range filter in ISO format"),
    end_time: Optional[str] = Query(None, description="End time for range filter in ISO format"),
    service: NotificationService = Depends(get_notification_service)
):
    try:
        notification = service.get_view_notification(tenant_id, product_id, start_time, end_time)
        return notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notify/purchase")
def get_purchase_notification(
    tenant_id: str,
    product_id: str,
    start_time: Optional[str] = Query(None, description="Start time for range filter in ISO format"),
    end_time: Optional[str] = Query(None, description="End time for range filter in ISO format"),
    service: NotificationService = Depends(get_notification_service)
):
    try:
        notification = service.get_purchase_notification(tenant_id, product_id, start_time, end_time)
        return notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
