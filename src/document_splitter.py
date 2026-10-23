from typing import List, Dict, Any
from langchain_core.documents import Document


class RecursiveTextSplitter():
    def __init__(self,
                 chunk_size=2000,
                 overlap_size=100) -> None:
        self.chunk_size: int = chunk_size
        self.overlap_size: int = overlap_size
        self.separators: List[str] = ["\n\n", "\n", " "]

    def split_documents(self, documents: List[Document]) -> None:
        container: List[Document] = []

        for text in documents:

            container.extend(self.text_splitter(text.page_content, self.separators, text.metadata["source"]))

        return container

    def text_splitter(self,
                      text: str,
                      sep: List[str], 
                      source: str,
                      start_index: int = 0) -> Document:

        if (len(text) <= self.chunk_size):
            return [Document(page_content=text,
                            metadata={"source": source,
                                      "first_character_index": start_index,
                                      "last_character_index":len(text)-1})]

        chunks: List[Document] = []
        splits = text.split(sep[0])

        for split in splits:

            if not split:
                continue

            split = split + sep[0]
            end_index = len(split) - 1
            if len(split) > self.chunk_size:
                chunks += self.text_splitter(split, sep[1:], source, start_index)
            else:
                chunks.append(Document(page_content=split,
                                       metadata={"source": source,
                                                 "first_character_index": start_index,
                                                 "last_character_index":end_index}))

            start_index = end_index + 1

        return chunks                


class PythonSplitter():
    def __init__(self, dotpy: List) -> None:
        pass

    def split(self) -> None:
        pass
