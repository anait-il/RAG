from pathlib import Path
from typing import Dict, List, Any


class Document():
    def __init__(self) -> None:
        pass


class DocumentLoader():
    def __init__(self, dir: str) -> None:
        self.dir: str = dir

    def load(self) -> Dict[List[Path], Any]:
        documents: Dict = {}
        text: List = []
        md: List = []
        py: List = []
        p: Path = Path(self.dir)
        for element in p.glob("*/*"):

            if element.suffix == ".txt":
                text.append(element)
            elif element.suffix == ".md":
                md.append(element)
            elif element.suffix == ".py":
                py.append(element)

        print(f"Start Loading...")
        for doc in md:
            print(doc.resolve())

        documents["py"] = self.load_content(py)
        documents["txt"] = self.load_content(text)
        documents["md"] = self.load_content(md)

        return documents

    def load_content(self, files: List[Path]) -> List[str]:
        content: List[str] = []
        for file in files:

            with open(file) as f:
                content.append(f.read())

        return content


class TextLoad():
    pass
