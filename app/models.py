from pydantic import BaseModel, Field
from pydantic.types import StrictInt, StrictStr

from utils import rot13_encrypt


class Sentence(BaseModel):
    id: StrictInt = Field(
        default=...,
        example=10
    )
    text: StrictStr = Field(
        default=...,
        description='text contained in the sentence',
        example='super movie title'
    )


class SentenceWithCypher(Sentence):
    cyphered_text: StrictStr = Field(
        default=None,
        description='cyphered text with rot13',
        example='fhcre zbivr gvgyr'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cyphered_text = rot13_encrypt(self.text)
