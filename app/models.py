from pydantic import BaseModel, Field


class Sentence(BaseModel):
    id: int = Field(None, example=10)
    text: str = Field(
        default=None,
        description='text contained in the sentence',
        example='super movie title'
    )


class SentenceWithCypher(Sentence):
    cyphered_text: str = Field(
        default=None,
        description='cyphered text with rot13',
        example='fhcre zbivr gvgyr'
    )
