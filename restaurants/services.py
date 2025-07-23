from fastapi import HTTPException
import uuid
from restaurants import repository
from restaurants.schema import RestaurantResponse
import logging

logger = logging.getLogger(__name__)


def get_restaurant_name():
    """
    Get the restaurant name from the database.
    """
    try:
        data = repository.get_restaurant_names()
        if not data:
            logger.warning("No restaurants found in database.")
            raise HTTPException(status_code=404, detail="Restaurant not found.")
        return data
    except Exception as exc:
        logger.error(f"Error in get_restaurant_name: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant names.")

def get_restaurant(restaurant_id):
    if not restaurant_id:
        raise HTTPException(status_code=400, detail="Missing restaurant_id.")
    try:
        uuid.UUID(str(restaurant_id))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid restaurant_id format.")
    try:
        data = repository.get_restaurant_data(restaurant_id)
        if not data:
            logger.warning(f"Restaurant with id {restaurant_id} not found.")
            raise HTTPException(status_code=404, detail="Restaurant not found.")
        return RestaurantResponse(
            restaurant_id=data.id,
            restaurant_name=data.restaurant_name,
            cuisine=data.cuisine.split(",")[0] if data.cuisine else None,
            overall_rating=data.overall_rating,
            total_review_counts=data.total_review_counts,
            five_stars=data.five_stars,
            four_stars=data.four_stars,
            three_stars=data.three_stars,
            two_stars=data.two_stars,
            one_stars=data.one_stars,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error in get_restaurant: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant data.")

def fetch_restaurant_context(restaurant_id: str) -> str:
    try:
        restaurant = repository.get_restaurant_data(restaurant_id)
        if not restaurant:
            logger.warning(f"No context found for restaurant id {restaurant_id}.")
            return "No specific restaurant context available."
        return (
            f"Restaurant Name: {restaurant.restaurant_name}\n"
            f"Location: {restaurant.restaurant_location}\n"
            f"Cuisine: {restaurant.cuisine}\n"
            f"Rating: {restaurant.overall_rating} stars\n"
            f"Neighbourhood: {restaurant.neighbourhood}\n"
            f"Average Price: {restaurant.average_price}"
        )
    except Exception as exc:
        logger.error(f"Error in fetch_restaurant_context: {str(exc)}", exc_info=True)
        return "No specific restaurant context available."



