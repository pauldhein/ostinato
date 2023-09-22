from __future__ import annotations
from typing import Dict, Any, List
from dataclasses import dataclass

from . import KeyType, get_pitch_val, PITCHES, KEYS, KEY_TYPE_MAP


@dataclass
class Key:
    root: int
    mode: KeyType

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"KEY: ({PITCHES[self.root]}, {KEYS[self.mode]})"

    @classmethod
    def from_xml(cls, xml: Dict[str, Any]) -> Key:
        """
        This function parses out a key-signature object from MusicXML.

        :param xml: [Dict] Data from MusicXML representing an attribute tag
        :return: [Tuple] key-signature tuple of the form (root-pitch, key-mode, key-onset)
        """
        if not xml.tag == "key":
            raise RuntimeError(f"Unexpected tag when parsing key: {xml.tag}")

        if len(xml) > 2:
            # Unset key type if no data found
            return cls(-1, -1)

        mode = xml[1].text
        key_type = KEY_TYPE_MAP[mode]
        fifths = int(xml[0].text)
        key_root = (fifths + (3 * key_type)) % 12
        return cls(key_root, key_type)


class Harmony:
    chords: List[ProgressionChord]

    def __init__(self, h: List[ProgressionChord] = None) -> Harmony:
        self.chords = list() if h is None else h
        self.chord_pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.chord_pointer >= len(self.data):
            raise StopIteration

        next_chord = self.data[self.chord_pointer]
        self.chord_pointer += 1
        return next_chord

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"HARMONY: {'; '.join([str(pc) for pc in self.chords])}"

    def add(self, chord: ProgressionChord) -> None:
        self.chords.append(chord)

    def reset(self):
        self.chord_pointer = 0


@dataclass
class ProgressionChord:
    root: int
    kind: KeyType

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"({PITCHES[self.root]}, {KEYS[self.kind]})"

    @classmethod
    def from_xml(cls, xml: Dict[str, Any]) -> ProgressionChord:
        """
        This function parses out a harmony object from MusicXML.

        :param harmony: [List] Data from MusicXML representing a harmony tag
        :return: [Tuple] harmony tuple of the form (root-pitch, Harm-mode, Harm-onset)
        """
        alteration = int(xml[0][1].text) if len(xml[0]) > 1 else 0
        root_pitch = get_pitch_val(xml[0][0].text, alt=alteration)
        kind = KEY_TYPE_MAP[xml[1].text]
        return cls(root_pitch, kind)
