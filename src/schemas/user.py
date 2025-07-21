from pydantic import BaseModel, ConfigDict, UUID4


class UserDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    full_name: str
    email: str
