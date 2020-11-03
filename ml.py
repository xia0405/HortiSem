import spacy
from typing import Dict, List, Optional
from pydantic import BaseModel, Schema

nlp = spacy.load("M:/Projekt/HortiSem/tmp_model")

ENT_PROP_MAP = {
    "Kultur": "Kultur",
    "Erreger": "Schaderreger",
    "Mittel": "PS Mittel"
}

class RecordDataRequest(BaseModel):
    text: str
    language: str = "en"


class RecordRequest(BaseModel):
    recordId: str
    data: RecordDataRequest


class RecordsRequest(BaseModel):
    values: List[RecordRequest]


class RecordDataResponse(BaseModel):
    entities: List


class Message(BaseModel):
    message: str


class RecordResponse(BaseModel):
    recordId: str
    data: RecordDataResponse
    errors: Optional[List[Message]]
    warnings: Optional[List[Message]]


class RecordsResponse(BaseModel):
    values: List[RecordResponse]


class RecordEntitiesByTypeResponse(BaseModel):
    recordId: str
    data: Dict[str, List[str]]


class RecordsEntitiesByTypeResponse(BaseModel):
    values: List[RecordEntitiesByTypeResponse]