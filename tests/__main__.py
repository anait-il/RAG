from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


model_name = "Qwen/Qwen3-0.6B"
path = "vllm-0.10.1"

model = AutoModelForCausalLM.from_pretrained(model_name,
                                             torch_dtype="auto",
                                             device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline("text-generation",
                       model=model,
                       tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=hf_pipeline)


def load_documents():
    docs = []
    
    loader = DirectoryLoader(path,
                             glob=["**/*.txt", "**/*.md"],
                             show_progress=True,
                             silent_errors=True,
                             loader_cls=TextLoader)

    documents = loader.load()

    for document in documents:
        print(document.metadata)

    return documents

def split_documents(docs):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    for doc in docs:
        chunks += splitter.split_text(doc.page_content)
    print(f"split docs into {len(chunks)} chunk")
    
    return chunks

def main():
    print("\nhello from RAG...")

    prompt = "Explain what a vector database is in one sentence."
    docs = load_documents()
    chunks = split_documents(docs)


if __name__ == "__main__":
    main()
