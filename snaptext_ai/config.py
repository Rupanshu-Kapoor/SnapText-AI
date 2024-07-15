
# model constants
mistral_repo = "mistralai/Mistral-7B-Instruct-v0.2"
llama3_repo = "meta-llama/Meta-Llama-3-8B-Instruct"
embedding_repo = "BAAI/bge-large-en-v1.5"
encode_kwargs = {'normalize_embeddings': True}


# constants for google cloud documentai
service_key_path = "google-cloud-service-key.json"
project_id = "handwritting-recognisation"
location = "us" 
processor_id = "4ce6e3828b180cda"
mime_type = "image/jpeg"    
field_mask = "text,entities,pages.pageNumber"

mime_types = {
    ".pdf": "application/pdf",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",}


# constants for vector db
chunk_size = 1000
chunk_overlap = 200
top_k = 3
text = " "


UPLOAD_DIRECTORY = "uploads"