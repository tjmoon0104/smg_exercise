from fastapi import FastAPI, Path

from models import Sentence, SentenceWithCypher

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description="""
            This is a simple REST API containing two endpoints.
            This API allows you to get a sentence with the encrypted version of it (with rot13),
            but also add new sentences in the existing store.""",
    version='1.0.0',
)


@app.get('/sentences/{sentence_id}', response_model=SentenceWithCypher)
def get_sentences_sentence_id(sentence_id: int = Path(
    default=None,
    description="ID of sentence to return",
    alias='sentenceId')
) -> SentenceWithCypher:
    """
    Get a sentence and its encrypted version
    """
    pass


@app.post('/sentences/', response_model=SentenceWithCypher)
def post_sentences_(body: Sentence) -> SentenceWithCypher:
    """
    Add a new sentence to the store
    """
    pass
