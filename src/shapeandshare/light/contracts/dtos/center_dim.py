from pydantic import BaseModel


class CenterDim(BaseModel):
    offset: int
    itr: int
