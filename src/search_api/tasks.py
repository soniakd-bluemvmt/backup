from sqlalchemy.orm import Session
from search_api.db import SessionLocal
from search_api.models.resource import Resource, EmbeddingStatus
from search_api.vector_utils import get_embedding, search_similar_for_tenant
import logging

logger = logging.getLogger(__name__)

def embed_resource(resource_uuid):
    db: Session = SessionLocal()
    resource = None
    try:
        resource = db.query(Resource).filter(Resource.resource_uuid == resource_uuid).first()
        if not resource:
            logger.error(f"Resource {resource_uuid} not found for embedding.")
            return

        text = resource.resource_description or resource.resource_name
        embedding = get_embedding(text)

        resource.embedding = embedding
        resource.embedding_status = EmbeddingStatus.SUCCESS
        resource.status_detail = None

        db.commit()
        logger.info(f"Successfully embedded resource {resource_uuid}")

    except Exception as e:
        logger.error(f"Embedding failed for resource {resource_uuid}: {e}")
        if resource:
            resource.embedding_status = EmbeddingStatus.FAILED
            resource.status_detail = str(e)
            db.commit()
    finally:
        db.close()
