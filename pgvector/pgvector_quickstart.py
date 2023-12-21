import pinecone
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.vectorstores.pgvector import PGVector
from pgvector_service import PgvectorService
import os
import time

load_dotenv()


# --------------------------------------------------------------
# Load the documents
# --------------------------------------------------------------

loader = TextLoader(
    "../data/The Project Gutenberg eBook of A Christmas Carol in Prose; Being a Ghost Story of Christmas.txt"
)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

query = "The Project Gutenberg eBook of A Christmas Carol in Prose; Being a Ghost Story of Christmas"


"""
First, we compare to Pinecone, a managed vector store service.

"""


# --------------------------------------------------------------
# Create / Load the Pinecone index
# --------------------------------------------------------------

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
)

index_name = "demo-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
    pinecone_docsearch = Pinecone.from_documents(
        docs, embeddings, index_name="demo-index"
    )
else:
    pinecone_docsearch = Pinecone.from_existing_index(index_name, embeddings)

# --------------------------------------------------------------
# Query the index with LanChain
# --------------------------------------------------------------


def run_query_pinecone(docsearch, query):
    docs = docsearch.similarity_search(query, k=4)
    result = docs[0].page_content
    return result


def calculate_average_execution_time(func, *args, **kwargs):
    total_execution_time = 0
    num_runs = 10
    for _ in range(num_runs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Execute the function with its arguments
        end_time = time.time()
        execution_time = end_time - start_time
        total_execution_time += execution_time
    average_execution_time = round(total_execution_time / num_runs, 2)
    print(result)
    print(
        f"\nThe function took an average of {average_execution_time} seconds to execute."
    )
    return


calculate_average_execution_time(
    run_query_pinecone, docsearch=pinecone_docsearch, query=query
)


"""
Now, we compare to PGVector, an open source vector store service.

"""

# --------------------------------------------------------------
# Create a PGVector Store
# --------------------------------------------------------------

"""
Donwload postgresql to run locally:
https://www.postgresql.org/download/

How to install the pgvector extension:
https://github.com/pgvector/pgvector

Fix common installation issues:
https://github.com/pgvector/pgvector?tab=readme-ov-file#installation-notes
"""

COLLECTION_NAME = "The Project Gutenberg eBook of A Christmas Carol in Prose"

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "pgvector"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postres"),
)

# create the store
db = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    pre_delete_collection=False,
)

# load the store
pgvector_docsearch = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)

# --------------------------------------------------------------
# Query the index with PGVector
# --------------------------------------------------------------


def run_query_pgvector(docsearch, query):
    docs = docsearch.similarity_search(query, k=4)
    result = docs[0].page_content
    return result


calculate_average_execution_time(
    run_query_pgvector, docsearch=pgvector_docsearch, query=query
)


# --------------------------------------------------------------
# Add more collections to the database
# --------------------------------------------------------------

loader = TextLoader("../data/The Project Gutenberg eBook of Romeo and Juliet.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
new_docs = text_splitter.split_documents(documents)


COLLECTION_NAME_2 = "The Project Gutenberg eBook of Romeo and Juliet"

db = PGVector.from_documents(
    embedding=embeddings,
    documents=new_docs,
    collection_name=COLLECTION_NAME_2,
    connection_string=CONNECTION_STRING,
    pre_delete_collection=False,
)


# --------------------------------------------------------------
# Query the index with multiple collections
# --------------------------------------------------------------

pg = PgvectorService(CONNECTION_STRING)


def run_query_multi_pgvector(docsearch, query):
    docs = docsearch.custom_similarity_search_with_scores(query, k=4)
    result = docs[0][0].page_content
    print(result)


run_query_multi_pgvector(pg, query)

# --------------------------------------------------------------
# Delete the collection
# --------------------------------------------------------------
pg.delete_collection(COLLECTION_NAME)
pg.delete_collection(COLLECTION_NAME_2)

# --------------------------------------------------------------
# Update the collection
# --------------------------------------------------------------
pg.update_collection(docs=docs, collection_name=COLLECTION_NAME)
