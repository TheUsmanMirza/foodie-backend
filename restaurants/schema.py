from pydantic import BaseModel, Field
from uuid import UUID


class RestaurantResponse(BaseModel):
    """Response model for restaurant details."""
    restaurant_id: UUID = Field(..., description="Unique identifier for the restaurant.")
    restaurant_name: str = Field(..., description="Name of the restaurant.")
    overall_rating: float = Field(..., description="Overall rating of the restaurant.")
    total_review_counts: int = Field(..., description="Total number of reviews.")
    five_stars: int = Field(..., description="Number of 5-star reviews.")
    four_stars: int = Field(..., description="Number of 4-star reviews.")
    three_stars: int = Field(..., description="Number of 3-star reviews.")
    two_stars: int = Field(..., description="Number of 2-star reviews.")
    one_stars: int = Field(..., description="Number of 1-star reviews.")
    cuisine: str = Field(..., description="Cuisine type of the restaurant.")

class ErrorResponse(BaseModel):
    """Standard error response model for API errors."""
    error: str = Field(..., description="Error message.")
    status_code: int = Field(..., description="HTTP status code.") 

