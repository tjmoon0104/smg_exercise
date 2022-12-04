from fastapi import FastAPI, Path, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from models import Sentence, SentenceWithCypher

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description="""
            This is a simple REST API containing two endpoints.
            This API allows you to get a sentence with the encrypted version of it (with rot13),
            but also add new sentences in the existing store.""",
    version='1.0.0',
)

sentence_dict = {
    1: {
        "id": 1,
        "text": "Text sample"
    },
    2: {
        "id": 2,
        "text": "Hello world"
    },
    3: {
        "id": "3",
        "text": "ID is string"
    },
    4: {
        "id": 4,
        "text": 1234
    },
    5: {
        "id": None,
        "text": "ID is null"
    },
    6: {
        "id": 6,
        "text": None
    },
}


# Override 422 RequestValidationError to 405
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content=jsonable_encoder({"detail": "Invalid input"}),
    )


@app.get('/sentences/{sentence_id}', response_model=SentenceWithCypher, status_code=status.HTTP_200_OK)
def get_sentences_sentence_id(sentence_id: int = Path(
    default=None,
    description="ID of sentence to return",
)) -> SentenceWithCypher:
    """
    Get a sentence and its encrypted version
    """
    if sentence_id not in sentence_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sentence not found")
    try:
        encrypted_sentence = SentenceWithCypher(**sentence_dict[sentence_id])
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID supplied")
    return encrypted_sentence


@app.post('/sentences/', response_model=SentenceWithCypher, status_code=status.HTTP_200_OK)
def post_sentences_(body: Sentence):
    """
    Add a new sentence to the store
    """
    return body
