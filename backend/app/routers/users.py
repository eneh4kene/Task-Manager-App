# here we create the routes for user creation (registration)
# - router to create the end point, serializer to receive and validate data, db session to enable database connection for data retrieval
from fastapi import APIRouter, Depends
from backend.app.models import User
from backend.app.shemas import UserResponse
from backend.app.auth_dependency import get_current_active_user

# initialize the router
router = APIRouter()


# route for reading user profile
@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user