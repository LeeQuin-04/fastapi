from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import Boolean, Column, Integer, String, Text, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DB_URL = "sqlite:///./todos.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
sessionLoacl = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
	pass

class TodoModel(Base):
	__tablename__ = "todos"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False)
	description = Column(Text, nullable=True)
	completed = Column(Boolean, default=False)
	priority = Column(Integer, default=1)

def get_db():
	db = sessionLoacl()
	try:
		yield db
	finally:
		db.close()

class TodoBase(BaseModel):
	title: str = Field(..., min_length=1, max_length=255)
	description: Optional[str] = None
	completed: bool = False
	priority: int = Field(default=1, ge=1, le=5)

	@field_validator("title")
	@classmethod
	def title_must_not_be_blank(cls, v: str) -> str:
		if not v.strip():
			raise ValueError("Tieu de phai chua ky tu ban nhe!")
		return v.strip()

	@model_validator(mode="after")
	def check_descrip_for_high_priority(self) -> "TodoBase":
		if self.priority >=3 and not self.description:
			raise ValueError(" Muc uu tien cao hon 3 phai co mo ta nhe ban")
		return self

class TodoCreate(TodoBase):
	pass

class TodoUpdate(BaseModel):
	title: Optional[str] = Field(None, min_length=1, max_length=255)
	description:Optional[str] = None
	completed: Optional[bool] = None
	priority: Optional[int] = Field(None, ge=1, le=5)

	@field_validator("title")
	@classmethod
	def title_must_not_be_blank(cls, v:Optional[str]) -> Optional[str]:
		if v is not None and not v.strip():
			raise ValueError("Tieu de phai chua ky tu ban oii")
		return v.strip() if v else v

class TodoResponse(TodoBase):
	id:int

	class Config:
		from_attribute = True

@asynccontextmanager
async def lifespan(app:FastAPI) -> AsyncGenerator:
	Base.metadata.create_all(bind=engine)
	yield

app = FastAPI(title="Todo API", lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/health/live", tags=["Health"])
def liveness():
	return {"status": "Song rat khoe"}

@app.get("/health/ready", tags=["Health"])
def readiness(db:Session = Depends(get_db)):
	try:
		db.execute(text("SELECT 1"))
		return {"status": "San sang", "database": "Da ket noi"}
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail=f"Loi db: {str(e)}",
		)

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["Todos"])
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
	db_todo = TodoModel(**todo.model_dump())
	db.add(db_todo)
	db.commit()
	db.refresh(db_todo)
	return db_todo

@app.get("/todos", response_model=List[TodoResponse], tags=["Todos"])
def get_todos(skip: int=0, limit:int=10, db: Session = Depends(get_db)):
	return db.query(TodoModel).offset(skip).limit(limit).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def get_todo_detail(todo_id:int, db:Session = Depends(get_db)):
	todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
	if not todo:
		raise HTTPException(status_code=404, detail="Todo nay khong ton tai")
	return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse, tags = ["Todos"])
def update_todo(todo_id:int, todo_data: TodoUpdate, db: Session=Depends(get_db)):
	db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
	if not db_todo:
		raise HTTPException(status_code=404, detail="Todo nay khong ton tai")
	for key, value in todo_data.model_dump(exclude_unset=True).items():
		setattr(db_todo, key, value)
	db.commit()
	db.refresh(db_todo)
	return db_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
def delete_todo(todo_id:int, db:Session=Depends(get_db)):
	db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
	if not db_todo:
		raise HTTPException(status_code=404, detail="Todo nay khong ton tai")
	db.delete(db_todo)
	db.commit()
	return None
TodoUpdate.model_rebuild()
