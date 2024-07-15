from snaptext_ai.rag_pipeline import RagPipeline
from snaptext_ai.document_ai import DocumentAI
from snaptext_ai.config import mistral_repo, UPLOAD_DIRECTORY, mime_types
import streamlit as st
from streamlit_chat import message
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from PIL import Image
import base64, os
from pathlib import Path
from dotenv import load_dotenv

# creating output directory if not exist
upload_dir = Path(UPLOAD_DIRECTORY)
Path.mkdir(upload_dir, exist_ok=True)

# setting page config
st.set_page_config(
        page_title="SnapText AI",
        page_icon="🤖",
        layout="wide"
    )

# creating prompt template
prompt = ChatPromptTemplate.from_template("""
You are a text completion assistant. 
Your task is to complete broken or partially parsed text while retaining the original context. 
Do not add any new information or content beyond what is necessary to make the text look like it was parsed completely efficiently. 
Do not repeat the same text.
Only fill in the missing parts or correct the incomplete segments based on the given context and add spaces and punctuation based on the context. 
Provide only the completed text as output, with no additional commentary.
Broken text: {broken_text}
Answer:
""")
output_parser = StrOutputParser()

# loading model
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(repo_id=mistral_repo, temperature=0.1)

# creating chain
chain = prompt|llm|output_parser


def main():

    st.header("SnapText AI")
    
    with st.sidebar:
        st.title("Settings")
        user_input = st.text_input("Enter your query: ", key="user_input")

    if user_input:
        with st.spinner("thinking..."):
            response = chain.invoke({"broken_text":user_input})
    
    doc_ai = DocumentAI()
    rag_pipeline = RagPipeline()

    image_col, extracted_text_col = st.columns(2)

    with image_col:
        with st.container(height=500, border=True):
            uploaded_files  = st.file_uploader(label="Upload file for OCR", type=["pdf", "JPEG", "JPG", "PNG"],accept_multiple_files=True)
            extracted_text = str()
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = upload_dir.joinpath(uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    #  Display images
                    if uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
                        image = Image.open(uploaded_file)
                        st.image(image, caption=uploaded_file.name)

                    #  Display PDFs
                    elif uploaded_file.type == "application/pdf":
                        st.markdown(f"#### {uploaded_file.name}")
                        pdf_data = uploaded_file.read()
                        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

                    extracted_text += doc_ai.document_ocr(file_path) + "\n\n"
    
    with extracted_text_col:
        with st.container(height=500, border=True):
            if uploaded_files:
                response =chain.invoke({"broken_text":extracted_text})

                st.write(response)

                # add function to pass the pdf file to the ocr function
    
    with st.container(height=300, border=True):
        prompt = st.chat_input("Ask from document")


# st.write("Made with ❤️ by [Rupanshu Kapoor](https://github.com/rupanroy)")
if __name__ == "__main__":
    main()