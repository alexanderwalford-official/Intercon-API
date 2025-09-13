from pydantic import BaseModel

class DictItem (BaseModel):
    uid: str
    oid: str
    data: dict

class DictItemGet(BaseModel):
    uid: str
    oid: str