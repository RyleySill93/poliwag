from poliwag.common.nanoid import NanoId

from pydantic import BaseModel, Extra


class BaseDomain(BaseModel):
    def to_dict(self):
        return self.dict()

    @classmethod
    def new(cls, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = NanoId.gen()

        return cls(**kwargs)

    class Config:
        orm_mode = True
        extra = Extra.forbid
        use_enum_values = True
