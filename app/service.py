from google.cloud import bigquery

from models import Sentence

client = bigquery.Client()


def search_sentence_from_storage(sentence_id):
    sql_query = f"""
    SELECT id, text FROM `fastapi-320118.sentences.sentences` WHERE id={sentence_id}
    """
    query_job = client.query(sql_query)
    return query_job.result()


def insert_sentence_to_storage(sentence: Sentence):
    # sql_query = f"""
    #     INSERT INTO `fastapi-320118.sentences.sentences`(id, text)
    #     WITH s AS (SELECT {sentence.id} id, '{sentence.text}' text)
    #     SELECT id, text FROM s WHERE NOT EXISTS(
    #     SELECT * FROM `fastapi-320118.sentences.sentences` t WHERE t.id=s.id)
    # """
    # query_job = client.query(sql_query)
    # return query_job.result()
    table = client.get_table("fastapi-320118.sentences.sentences")
    errors = client.insert_rows(
        table=table,
        rows=[{"id": sentence.id, "text": sentence.text}]
    )
    if errors:
        raise Exception("Something happened with the Storage server")


def delete_sentence_from_storage(sentence_id):
    """Doesn't work because of stream buffer"""
    sql_query = f"""
    DELETE FROM `fastapi-320118.sentences.sentences` where id={sentence_id}
    """
    query_job = client.query(sql_query)
    return query_job.result()


def get_max_id_from_storage() -> int:
    sql_query = """
    SELECT MAX(id) as id
    FROM `fastapi-320118.sentences.sentences`
    LIMIT 1
    """
    query_job = client.query(sql_query)
    first_row = next(query_job.result())
    return first_row[0]
