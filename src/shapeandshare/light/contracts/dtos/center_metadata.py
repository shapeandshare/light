from pydantic import BaseModel

from .center_dim import CenterDim


class CenterMetadata(BaseModel):
    x: CenterDim
    y: CenterDim
