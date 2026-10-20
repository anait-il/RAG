from typing import List, Dict, Any
from langchain_core.documents import Document


class TextSplitter():
    def __init__(self,
                 dotmd: List,
                 dotxt: List,
                 chunk_size=2000,
                 overlap_size=100) -> None:
        self.dotmd: List[Document] = dotmd
        self.dotxt: List[Document] = dotxt
        self.chunk_size: int = chunk_size
        self.overlap_size: int = overlap_size
        self.separators: List[str] = ["\n\n", "\n", " ", ""]

    def split(self) -> None:
        container: List[Document] = []
        data: List[Document] = self.dotmd

        for text in data:
            container.extend(self.recursive_text_splitter(text))

    def recursive_text_splitter(self,
                                text: str,
                                sep: str, 
                                metadata: Dict[str, str]) -> Document:
        chunks: List[Document] = []
        start_index: int = 0

        for index, char in enumerate(text):
            if char == sep:
                if index > self.chunk_size:
                    self.recursive_text_splitter(text, next(self.separators))            
                else:
                    chunks.append(Document(page_content=text[start_index:index+1],
                                           metadata=metadata))
                    start_index = index+1
                


class PythonSplitter():
    def __init__(self, dotpy: List) -> None:
        pass

    def split(self) -> None:
        pass
