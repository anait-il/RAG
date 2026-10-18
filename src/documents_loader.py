from pathlib import Path
from typing import Dict, List


class Document():
    def __init__(self) -> None:
        pass


class DocumentLoader():
    def __init__(self, dir: str) -> None:
        self.dir: str = dir

    def load(self) -> Dict[List[Path]]:
        documents: Dict = {}
        text: List = []
        md: List = []
        py: List = []
        p: Path = Path(self.dir)
        for element in p.glob("*/*"):

            if element.suffix() == ".txt":
                text.append(element)
            elif element.suffix() == ".md":
                md.append(element)
            elif element.suffix() == ".py":
                py.append(element)

        documents["py"] = py
        documents["txt"] = text
        documents["md"] = md

        return documents


class TextLoad():
    pass
