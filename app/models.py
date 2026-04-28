from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.database import Base

#Model table task for DB
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    status = Column(String(30), nullable=False, default="pending")
    category = Column(String(30), nullable=False, default="personal")
    deadline = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)