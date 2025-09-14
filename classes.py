from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class DictItem (BaseModel):
    api_key: str
    uid: str
    oid: str
    data: dict

class DictItemGet(BaseModel):
    api_key: str
    uid: str
    oid: str

class DataItemTable(BaseModel):
    api_key: str
    action: str ## SELECT 
    identifier: str ## COL
    table: str ## FROM TABLE
    match: str ## WHERE VAL

class DataItemTableSave(BaseModel):
    api_key: str
    uid: str
    table: str
    cols: str
    vals: str

class QueryItem(BaseModel):
    query: str

class SaveDataItem(BaseModel):
    api_key: str
    uid: str
    file_name: str
    file_content: str
    folder: str
    notes: str


class SaveDataItemGet(BaseModel):
    api_key: str
    uid: str