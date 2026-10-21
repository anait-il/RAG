from typing import List, Dict, Any
from langchain_core.documents import Document


class RecursiveTextSplitter():
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

            container.extend(self.text_splitter(text.page_content, self.separators, text.metadata["source"]))

        return container

    def text_splitter(self,
                      text: str,
                      sep: List[str], 
                      source: str,
                      start_index: int = 0) -> Document:

        chunks: List[Document] = []
        splits = text.split(sep[0])

        for split in splits:

            end_index = len(split) - 1
            if len(split) > self.chunk_size:
                chunks += self.text_splitter(split, sep[1:], source, start_index)
            else:
                chunks.append(Document(page_content=split,
                                       metadata={"source": source,
                                                 "first_character_index": start_index,
                                                 "last_character_index":end_index})) 
            start_index = end_index + 1
 
        # for index, char in enumerate(text):
        #     print(sep[0])
        #     if char == sep[0]:
        #         print(sep)
        #         if index > self.chunk_size:
        #             chunks += self.text_splitter(text[start_index:index+1], sep[1:])      
        #         else:
        #             chunks.append(Document(page_content=text[start_index:index+1],
        #                                    metadata={"source": source,
        #                                              "first_character_index": start_index,
        #                                              "last_character_index": index}))
        #             start_index = index+1

        return chunks                


class PythonSplitter():
    def __init__(self, dotpy: List) -> None:
        pass

    def split(self) -> None:
        pass
