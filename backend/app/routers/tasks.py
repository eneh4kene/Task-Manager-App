# we create a new route for creating a new task. It's going to be a protected route so only registered users can acces it
# we need a router to create the route, we need a serializer to format and validate the task data, we need a database connection,
# we need authentication (jwt) dependes to protect the endpoints
from fastapi import APIRouter, Depends, HTTPException
from backend.app.database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.auth_dependency import get_current_active_user
from backend.app.models import User, Task
from backend.app.shemas import TaskCreate, TaskResponse, TaskUpdate



# create the router
router = APIRouter()

# route for creating task
@router.post("/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db), 
                current_user: User=Depends(get_current_active_user)):
    new_task = Task(title=task_data.title,
                    description=task_data.description,
                    completed=task_data.completed,
                    owner_id=current_user.id)
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# route for reading tasks (with optional query parameters to filter tasks by search)
@router.get("/", response_model= List[TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user),
              query_string: Optional [str] = None):
    tasks_query = db.query(Task).filter(Task.owner_id == current_user.id)
    if query_string:
        search = f"%{query_string}%"
        tasks_query = tasks_query.filter(
            (Task.title.ilike(search)) | (Task.description.ilike(search))
        )
    # return all the queries as response
    tasks = tasks_query.all()

    return tasks


# route for updating a specific task
@router.put("/{task_id}", response_model = TaskResponse)
def update_a_task(task_id: int, task_data: TaskUpdate, current_user: User = Depends(get_current_active_user), 
                  db: Session = Depends(get_db)):
    # find the task matching the id, and if it belongs to the user/is authorized,
    #  update it and send the response back
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or user not authorized to access task")
    
    if task_data.title:
        task.title = task_data.title
    if task_data.description:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # save andd refresh
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# route for deleting a specific task
@router.delete("/{task_id}")
def delete_a_task(task_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # find the matching task and delete if user is authorized to access it
    task_to_delete = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="task not found or user not authorized to delete task")
    
    db.delete(task_to_delete)
    db.commit()

    return {"message" : "Task has been deleted successfully"}
