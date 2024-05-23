from pydantic import BaseModel

class UserSchemaCreate(BaseModel):
    username:str
    password:str
    # telegram_id: int| None = None