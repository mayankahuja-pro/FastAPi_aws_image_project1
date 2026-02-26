# FastAPI aur zaroori cheezein import kar rahe hain
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import uuid  # Unique ID banane ke liye

# Apne project ke modules import kar rahe hain
from .database import SessionLocal, engine, Base
from .models import ImageUpload              # DB ka table model
from .s3_service import upload_file_to_s3   # S3 pe file upload karne ka function

# Saari tables database mein create kar do (agar exist nahi karti)
Base.metadata.create_all(bind=engine)

# FastAPI app ka instance banaya, title diya
app = FastAPI(title="Image Upload API")


# DB session dene wala dependency function
def get_db():
    db = SessionLocal()   # Naya DB session kholo
    try:
        yield db          # Route function ko session do
    finally:
        db.close()        # Kaam hone ke baad session band karo


# POST endpoint - image upload karne ke liye
@app.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),       # User se file lo
    db: Session = Depends(get_db),      # DB session inject karo
):
    # File ka extension nikalo (jaise .jpg, .png)
    file_ext = file.filename.split(".")[-1]

    # Har baar ek naya unique naam banao taaki conflict na ho
    unique_filename = f"{uuid.uuid4()}.{file_ext}"

    # File ko AWS S3 bucket pe upload karo aur URL wapas lo
    file_url = upload_file_to_s3(
        file.file,          # File ka actual data
        unique_filename,    # S3 pe store hone wala naam
        file.content_type,  # File ka type (image/jpeg etc.)
    )

    # S3 URL ko database mein save karo
    new_image = ImageUpload(file_url=file_url)
    db.add(new_image)       # Record add karo
    db.commit()             # Save karo database mein
    db.refresh(new_image)   # Latest data wapas lo

    # Success response bheji - URL aur upload time ke saath
    return {
        "message": "Upload successful",
        "file_url": file_url,
        "uploaded_at": new_image.uploaded_at,
    }
