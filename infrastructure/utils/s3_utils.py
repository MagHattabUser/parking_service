from minio import Minio
from web.config import Configs

config = Configs()

def get_minio_client():
    return Minio(
        config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=config.MINIO_SECURE
    )

def list_bucket_files():
    client = get_minio_client()
    try:
        objects = client.list_objects(config.BUCKET_NAME)
        return [obj.object_name for obj in objects]
    except Exception as e:
        print(f"Error listing bucket files: {e}")
        return []

def get_image_from_minio(object_name: str) -> bytes:
    client = get_minio_client()
    try:
        data = client.get_object(config.BUCKET_NAME, object_name)
        return data.read()
    except Exception as e:
        raise Exception(f"Error getting image from MinIO: {e}")

def upload_to_minio(file_path: str, object_name: str) -> str:
    client = get_minio_client()
    try:
        client.fput_object(config.BUCKET_NAME, object_name, file_path)
        return f"https://{config.MINIO_ENDPOINT}/{config.BUCKET_NAME}/{object_name}"
    except Exception as e:
        raise Exception(f"Error uploading to MinIO: {e}") 