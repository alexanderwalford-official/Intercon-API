from pydantic import BaseModel

class DictItem (BaseModel):
    uid: str
    data: dict