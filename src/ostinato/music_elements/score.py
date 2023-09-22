from __future__ import annotations
from zipfile import ZipFile
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from xml.etree.ElementTree import parse

from . import MLOG, Part


@dataclass
class Score:
    parts: List[Part]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        parts = "\n".join(
            [f"PART {i+1}:\n{str(p)}" for i, p in enumerate(self.parts)]
        )
        return f"SCORE\n{parts}"

    @classmethod
    def from_xml(cls, xml: Dict[str, Any]) -> Score:
        MLOG.debug("Parsing score")
        part_xml, part_list_xml = list(), None
        for element in xml:
            if element.tag == "part-list":
                part_list_xml = element
            elif element.tag == "part":
                part_xml.append(element)

        parts = list()
        for i, (p, pl) in enumerate(zip(part_xml, part_list_xml)):
            MLOG.debug(f"Parsing part #{i+1}")
            parts.append(Part.from_xml(p, pl))

        return cls(parts)

    @classmethod
    def from_xml_file(cls, filepath: str) -> Score:
        filename = filepath[filepath.rfind("/") + 1 :]
        MLOG.debug(f"Validating file `{filename}`")
        if filepath.endswith(".mxl"):
            MLOG.debug("Unzipping MusicXML data")
            z = ZipFile(filepath, "r")
            files = [
                f for f in z.namelist() if f.endswith(".xml") and "/" not in f
            ]
            filepath = z.extract(files[0], path="./extracted_xml/")
        elif not filepath.endswith(".xml"):
            raise RuntimeError(f"Unsupported music file type: {filepath}")

        xml_data = parse(filepath).getroot()
        return cls.from_xml(xml_data)

    def to_siatec_score(self, part_num: int) -> List[Tuple[int, float]]:
        return self.parts[part_num - 1].to_siatec_score()
