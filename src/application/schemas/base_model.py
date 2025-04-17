from pydantic import BaseModel, ConfigDict


class BaseModelMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)