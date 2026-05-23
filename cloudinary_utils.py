import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_to_cloudinary(filepath):
    result = cloudinary.uploader.upload_large(
        filepath,
        resource_type="video"
    )

    return result["secure_url"], result["public_id"]

def delete_cloudinary(public_id):
    cloudinary.uploader.destroy(
        public_id,
        resource_type="video"
    )