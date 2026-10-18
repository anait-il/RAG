from transformers import AutoModelForCausalLM, AutoTokenizer
from .documents_loader import DocumentLoader, Document
from typing import List, Dict, Any


def main():

    path: str = "vllm-0.10.1"
    #Load .py files
    doc_loader = DocumentLoader(path)
    documents: List[Document] = doc_loader.load()


if __name__ == "__main__":
    main()
