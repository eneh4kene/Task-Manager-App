from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.auth import router as auth_router
from backend.app.routers.users import router as users_router
from backend.app.routers.tasks import router as tasks_router
from backend.app.database import engine, Base


# create the fastapi app instance
app = FastAPI()

# CORS configuration (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables on startup (optional, for development purposes)
Base.metadata.create_all(bind=engine)


# register the routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Root for health check
@app.get("/")
def root():
    return {"message" : "welcome to the task manager app"}