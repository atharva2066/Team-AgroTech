# app/utils/helpers.py

from typing import Any, Dict, List
from bson import ObjectId


def serialize_mongo_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc

    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc


def serialize_mongo_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [serialize_mongo_document(doc) for doc in docs]