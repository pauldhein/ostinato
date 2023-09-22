from __future__ import annotations
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

from tqdm import tqdm

from . import Measure, MLOG, Rest, Note


@dataclass
class Part:
    instrument: str
    measures: List[Measure]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        measures = "\n".join(
            [f"MEASURE {i+1}:\n{str(m)}" for i, m in enumerate(self.measures)]
        )
        return f"INSTRUMENT: {self.instrument}\n{measures}"

    @classmethod
    def from_xml(
        cls, part_xml: Dict[str, Any], meta_xml: Dict[str, Any]
    ) -> Part:
        measures = [
            Measure.from_xml(measure)
            for measure in tqdm(part_xml, desc="Parsing measures")
        ]

        # MLOG.debug("Reforming cross-measure notes")
        # for m1, m2 in tqdm(
        #     zip(measures[:-1], measures[1:]),
        #     desc="Reforming cross-measure notes",
        # ):
        #     if not m1.melody.notes:
        #         continue  # Skip empty measures from editing

        #     n1 = m1.melody.notes[-1]
        #     n2 = m2.melody.notes[0]
        #     both_rests = isinstance(n1, Rest) and isinstance(n2, Rest)
        #     both_notes = isinstance(n1, Note) and isinstance(n2, Note)
        #     if both_rests or (both_notes and n1.pitch == n2.pitch):
        #         m2.melody.notes.pop(0)
        #         m1.melody.notes[-1].duration = n1.duration + n2.duration

        MLOG.debug("Finding instrument data for part")
        instrument = meta_xml.find("score-instrument")
        instrument_name = instrument.find("instrument-name").text
        return cls(instrument_name, measures)

    def to_siatec_score(self) -> List[Tuple[int, float]]:
        return [n for m in self.measures for n in m.to_siatec_score()]
