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
    def __init__(self, chunk_size=2000, overlap_size=100) -> None:
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.separators = ["class", "def", 'if __name__ == "__main__"']

    def split_documents(self, documents: List[Document]) -> None:
        container: List[Document] = []

        for code in documents:

            container.extend(self.code_splitter(code.page_content, self.separators, code.metadata["source"]))

        return container[::-1]
    
    def code_splitter(self,
                        code: str,
                        sep: List[str], 
                        source: str) -> Document:

        if (len(code) <= self.chunk_size):
            return [Document(page_content=code,
                             metadata={"source": source,
                                        "first_character_index": 0,
                                        "last_character_index":len(code)-1})]

        chunks: List[int] = []
        if not chunks:
            end_index = len(code) - 1

        while end_index > 0:
            start_index = code[:end_index].rfind(sep[0])
            if start_index == -1:
                start_index = 0

            chunk = code[start_index: end_index]
            if not chunk:
                break

            if len(chunk) > self.chunk_size:
                if len(sep) == 1:
                    start_index = end_index - self.chunk_size
                    chunks.append(Document(page_content=code[start_index: end_index],
                                           metadata={"source": source,
                                                     "first_character_index": start_index,
                                                     "last_character_index": end_index}))
                    end_index = start_index - 1

                else:
                    chunks += self.code_splitter(chunk, sep[1:], source)

            else:
                chunks.append(Document(page_content=chunk,
                                      metadata={"source": source,
                                                "first_character_index": start_index,
                                                "last_character_index": end_index}))

            end_index = start_index - 1

        return chunks
