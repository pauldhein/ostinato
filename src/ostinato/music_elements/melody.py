from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Union
from dataclasses import dataclass

from . import Duration, assign_dur_label, get_pitch_val, PITCHES


@dataclass
class Melody:
    notes: List[MelodyElement]

    def __post_init__(self):
        self.note_pointer = 0

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"MELODY: {'; '.join([str(n) for n in self.notes])}"

    def __iter__(self):
        return self

    def __next__(self):
        if self.note_pointer >= len(self.notes):
            raise StopIteration

        next_note = self.notes[self.note_pointer]
        self.note_pointer += 1
        return next_note

    @classmethod
    def from_xml(cls, xml: Dict[str, Any]) -> Melody:
        melody = list()
        sum_dur = 0
        for element in xml:
            element = MelodyElement.parse_music_element(element)

            # Remove chord elements
            if not element:
                continue

            (_, dur) = element

            sum_dur += dur
            melody.append(element)

        measure_dur = 0
        new_melody = list()
        for (midi, dur) in melody:
            onset = measure_dur / sum_dur
            measure_dur += dur
            duration = Duration(dur / sum_dur)
            if midi != -1:
                new_note = Note(duration, onset, midi)
            else:
                new_note = Rest(duration, onset)
            new_melody.append(new_note)

        return cls(new_melody)

    def to_siatec_score(self) -> List[Tuple[int, float]]:
        return [note.to_siatec_score() for note in self.notes]


@dataclass
class MelodyElement(ABC):
    duration: Union[int, Duration]
    onset: float

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @staticmethod
    def parse_music_element(element: Dict[str, Any]) -> Tuple[int, int]:
        """
        This function parses out a musical object from MusicXML. The musical object
        can be either the representation of a Note, Rest, or Chord.

        :param music_el: [List] Data from MusicXML representing a note tag
        :return: [Tuple] music object of the form (type, pitch, duration, note-onset)
        """
        if element.find("chord"):
            return None  # Not handling chords

        pitch = element.find("pitch")
        rest = element.find("rest")
        duration = int(element.find("duration").text)
        if rest is not None:
            midi = -1
        else:
            step = pitch.find("step").text
            octave = int(pitch.find("octave").text)
            alter = pitch.find("alter")
            alteration = float(alter.text) if alter else 0
            midi = get_pitch_val(step, octave, alteration)

        return (midi, duration)

    @abstractmethod
    def to_siatec_score(self) -> Tuple[int, float]:
        pass


@dataclass
class Note(MelodyElement):
    pitch: int

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        root = PITCHES[self.pitch % 12]
        octave = self.pitch // 12
        return f"({root}{octave}, {self.duration})"

    def to_siatec_score(self) -> Tuple[int, float]:
        return (self.pitch, round(self.duration))


@dataclass
class Rest(MelodyElement):
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"(--, {self.duration})"

    def to_siatec_score(self) -> Tuple[int, float]:
        return (-1, round(self.duration))
