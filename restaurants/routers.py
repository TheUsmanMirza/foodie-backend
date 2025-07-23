import logging

from fastapi import APIRouter, Depends, HTTPException

from restaurants import services
from users.model import User
from users.utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/get_all_restaurants_name")
def get_all_restaurants_name():
    try:
        return services.get_restaurant_name()
    except Exception as exc:
        logger.error(f"Error fetching restaurant names: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant names.")


@router.get("/get_restaurant_data")
def get_restaurant(current_user: User = Depends(get_current_user)):
    try:
        return services.get_restaurant(current_user.restaurant_id)
    except Exception as exc:
        logger.error(f"Error fetching restaurant data: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant data.")
