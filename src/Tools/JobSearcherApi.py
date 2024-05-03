from langchain_openai import OpenAIEmbeddings
import os
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

atlas = os.getenv('ATLAS_URI')
# Connect to your Atlas cluster

client = MongoClient(atlas)
# Create embeddings 
embeddings = OpenAIEmbeddings(disallowed_special=())

# Configure settings for db use
db_name = "sample_jobs"
collection_name = "jobs"
namespace = db_name + "." + collection_name
vector_index = "vector_index"
text_key = "description"
embedding_key = "description_embedding"

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string = atlas,
    namespace = namespace,
    embedding = embeddings,
    index_name = vector_index,
    text_key = text_key,
    embedding_key = embedding_key
)

def search(position: str, city: str = "Porto") -> dict:
    query_filter = {"city": {"$eq": city}} if city else None

    docs = vector_search.similarity_search(query=position, pre_filter=query_filter)

    return _format(docs)

def _format(docs):
    results = {}
    for i, doc in enumerate(docs):
        vacancy = doc.metadata["vacancy"]
        city = ", ".join(doc.metadata["city"])
        employer = doc.metadata["employer"]
        formatted_string = f"Vacancy: {vacancy}, City: {city}, Employer: {employer}"
        results[f"{i+1}"] = formatted_string
    return results