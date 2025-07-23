from database import SessionLocal
from restaurants.model import Restaurant
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


def get_restaurant_names():
    """Get all restaurant names from the database."""
    try:
        with SessionLocal() as db:
            result = db.query(Restaurant.id, Restaurant.restaurant_name).all()
            return [{"id": r.id, "name": r.restaurant_name} for r in result]
    except Exception as exc:
        logger.error(f"Error in get_restaurant_names: {str(exc)}", exc_info=True)
        raise Exception("Failed to fetch restaurant names from the database.")


def get_restaurant_data(restaurant_id: UUID):
    """Get restaurant data by ID."""
    try:
        with SessionLocal() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if restaurant:
                return restaurant
    except Exception as exc:
        logger.error(f"Error in get_restaurant_data: {str(exc)}", exc_info=True)
        raise Exception("Failed to fetch restaurant data from the database.")


def get_existing_restaurant(restaurant_name: str, location: str):
    """Check if a restaurant already exists in the database."""
    try:
        with SessionLocal() as db:
            existing_restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_name == restaurant_name,
                Restaurant.restaurant_location == location
            ).first()
            return existing_restaurant
    except Exception as exc:
        logger.error(f"Error in get_existing_restaurant: {str(exc)}", exc_info=True)
        raise Exception("Failed to check for existing restaurant in the database.")


def update_restaurant(restaurant_data):
    """Update restaurant data in the database."""
    try:
        with SessionLocal() as db:
            for each in restaurant_data:
                restaurant_name = each.get("restaurant_name")
                restaurant = db.query(Restaurant).filter(Restaurant.restaurant_name == restaurant_name).first()
                if restaurant:
                    restaurant.overall_rating = each.get("overall_rating", restaurant.overall_rating)
                    restaurant.total_rating = each.get("total_rating", restaurant.total_rating)
                    restaurant.food_rating = each.get("food_rating", restaurant.food_rating)
                    restaurant.service_rating = each.get("service_rating", restaurant.service_rating)
                    restaurant.ambience_rating = each.get("ambience_rating", restaurant.ambience_rating)
                    restaurant.total_review_counts = each.get("total_review_count", restaurant.total_review_counts)
                    restaurant.five_stars = each.get("five_stars", restaurant.five_stars)
                    restaurant.four_stars = each.get("four_stars", restaurant.four_stars)
                    restaurant.three_stars = each.get("three_stars", restaurant.three_stars)
                    restaurant.two_stars = each.get("two_stars", restaurant.two_stars)
                    restaurant.one_stars = each.get("one_stars", restaurant.one_stars)
                    db.commit()
            return {"message": "Restaurant updated successfully"}
    except Exception as exc:
        logger.error(f"Error in update_restaurant: {str(exc)}", exc_info=True)
        raise Exception("Failed to update restaurant data.")
