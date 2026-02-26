# SQLAlchemy ke column types aur Base import kar rahe hain
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base  # Apna Base class lo jisse model inherit karega


# ImageUpload model - database mein "image_uploads" naam ki table banayega
class ImageUpload(Base):
    __tablename__ = "image_uploads"  # Table ka naam

    id = Column(Integer, primary_key=True, index=True)  # Har record ka unique ID
    file_url = Column(String, nullable=False)            # S3 pe file ka URL - ye zaroor chahiye
    uploaded_at = Column(DateTime, default=datetime.now)  # Upload time - automatically set hoga