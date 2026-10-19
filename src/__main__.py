from transformers import AutoModelForCausalLM, AutoTokenizer
from .documents_loader import DocumentLoader, Document
from .document_splitter import TextSplitter, PythonSplitter
from typing import List


def main():

    path: str = "vllm-0.10.1"
    #Load files
    doc_loader = DocumentLoader(path)
    documents: List[Document] = doc_loader.load()

    #chunking txt and md files
    text_splitter = TextSplitter(documents["txt"], documents["md"])
    chunks = text_splitter.split()

    #chunk python files
    py_splitter = PythonSplitter(documents["py"])
    py_chunks = py_splitter.split()

    #tokenizing


if __name__ == "__main__":
    main()
