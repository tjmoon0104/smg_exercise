from fastapi import FastAPI, Path, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from models import Sentence, SentenceWithCypher
from service import search_sentence_from_storage, insert_sentence_to_storage

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description="""
            This is a simple REST API containing two endpoints.
            This API allows you to get a sentence with the encrypted version of it (with rot13),
            but also add new sentences in the existing store.""",
    version='1.0.0',
)


# Override 422 RequestValidationError to 400 and 405
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for pydantic_error in exc.errors():
        # Error Info
        err_loc = pydantic_error.get('loc', '')
        err_msg = pydantic_error.get('msg', '')
        err_type = pydantic_error.get('type', '')

        # GET sentence error
        if {'path', 'sentence_id'}.issubset(err_loc):
            if 'type_error' in err_type:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=jsonable_encoder({"detail": f"Invalid ID supplied ({err_msg})"}),
                )
        # POST sentence error
        elif {'body'}.issubset(err_loc):
            if 'type_error' in err_type:
                return JSONResponse(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    content=jsonable_encoder({"detail": f"Invalid input ({err_msg})"}),
                )
    # Other errors
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": "Unknown Error"}),
    )


@app.get('/sentences/{sentence_id}',
         response_model=SentenceWithCypher, status_code=status.HTTP_200_OK)
def get_sentences_sentence_id(sentence_id: int = Path(
    default=None,
    description="ID of sentence to return",
)) -> SentenceWithCypher:
    """
    Get a sentence and its encrypted version
    """
    result = search_sentence_from_storage(sentence_id)
    if result.total_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sentence not found")
    # Get first row
    first_row = next(result)
    return SentenceWithCypher(**first_row)


@app.post('/sentences/', response_model=SentenceWithCypher, status_code=status.HTTP_200_OK)
def post_sentences_(body: Sentence):
    """
    Add a new sentence to the store
    """
    search_result = search_sentence_from_storage(body.id)
    if search_result.total_rows != 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sentence ID exists")
    else:
        try:
            insert_sentence_to_storage(body)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Something happened with the Storage server")
    return body
