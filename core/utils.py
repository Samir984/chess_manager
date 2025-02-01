from typing import Any
from cloudinary import uploader # type: ignore
from ninja import UploadedFile
from ninja.errors import HttpError
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def handle_upload_to_cloudinary(
    image: UploadedFile,
    folder: str = "reports",
)->Any:
    try:
        if image.size > MAX_FILE_SIZE:
            raise ValueError("File too large (max 5MB)")

        # Read and upload file
        image_data = image.read()
        result = uploader.upload( # type: ignore
            image_data, folder=folder, resource_type="auto"
        )
        return result

    except HttpError as e:
        raise e
    except Exception as e:
        raise HttpError(500, f"Image upload failed: {str(e)}")
