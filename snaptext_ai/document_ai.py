from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from typing import Optional
from dotenv import load_dotenv
import os
from .config import *
from pathlib import Path
import fitz


class DocumentAI:

    def __init__(self):
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(service_key_path)

        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.field_mask = field_mask

    def count_pdf_pages_pymupdf(self, file_path):

        doc = fitz.open(file_path)
        # return len(doc)
        return doc.page_count
    

    def document_ocr(self, file_path: str):

        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        name = client.processor_path(project_id, location, processor_id)
        with open(file_path, "rb") as image:
             image_content = image.read()

        # extract extension from file path
        extension = Path(file_path).suffix

        pages = [1]
        if extension == ".pdf":
            # count number of pages in pdf
            page_number = self.count_pdf_pages_pymupdf(file_path)
            pages = list(range(1, page_number + 1))

        mime_type = mime_types.get(extension)
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
        process_options = documentai.ProcessOptions(
                individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
                    pages=pages
                )
            )
        
        request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=self.field_mask,
        process_options=process_options,
    )

        result = client.process_document(request=request)
        return result.document.text




