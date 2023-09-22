from __future__ import annotations
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

from . import MLOG, Key, ProgressionChord, Melody, Harmony


@dataclass
class Measure:
    key: Key
    melody: Melody
    harmony: Harmony

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        key_str = str(self.key) if self.key else ""
        harmony_str = str(self.harmony) if self.harmony.chords else ""
        melody_str = str(self.melody) if self.melody.notes else ""

        res = ""
        if key_str != "":
            res += f"{key_str}\n"

        if harmony_str != "":
            res += f"{harmony_str}\n"

        if melody_str != "":
            res += f"{melody_str}\n"

        return res

    @classmethod
    def from_xml(cls, xml: Dict[str, Any]) -> Measure:
        """
        This function parses a MusicXML measure and transforms the data
        contained into it into three separate temporal lists. The lists
        represent the melody, harmony and key-signature as found in the
        measure. The lists are returned in a dictionary. This function contains
        subroutines that are used to parse the musical features that will be
        found in the XML for a measure.

        :param measure_data: [List] Data from MusicXML representing a musical measure
        :param measure_num: [Integer] The number of the current measure for use in setting offsets
        :return: [Measure] lists of all musical objects found, separated into melody, harmony, and key-signature
        """
        key = None
        harmony = Harmony()
        melody_xml = list()
        note_counter, harm_counter, key_counter = 0, 0, 0
        for music_el in xml:
            if music_el.tag == "note":
                note_counter += 1
                MLOG.debug(f"Parsing note #{note_counter}")
                melody_xml.append(music_el)
            elif music_el.tag == "harmony":
                harm_counter += 1
                MLOG.debug(f"Parsing harmony #{harm_counter}")
                harmony.add(ProgressionChord.from_xml(music_el))
            elif music_el.tag == "attributes":
                key_counter += 1
                MLOG.debug(f"Parsing key #{key_counter}")
                key = Key.from_xml(music_el.find("key"))

        return cls(key, Melody.from_xml(melody_xml), harmony)

    def to_siatec_score(self) -> List[Tuple[int, float]]:
        return self.melody.to_siatec_score()
