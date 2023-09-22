from __future__ import annotations
import logging

logging.basicConfig(
    format="[%(levelname)s] < %(filename)s:%(funcName)s():L%(lineno)d > — %(message)s"
)
MLOG = logging.getLogger("music-element-logger")


def enum(**args):
    return type("Enum", (), args)


KEYS = (
    "M",
    "m",
    "Mm",
    "A",
    "d",
    "D",
    "hd",
    "S4",
    "M6",
    "m6",
    "M7",
    "m7",
    "A7",
    "d7",
    "M9",
    "m9",
    "D9",
    "m11",
    "D13",
    "S2",
)

PITCHES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
# =============================================================================
# ENUM DEFINITIONS
# =============================================================================

KeyType = enum(
    UNSET=-1,  # Unset
    MAJOR=0,  # Major
    MINOR=1,  # Minor
    MAJMIN=2,  # Major-Minor
    AUGMENTED=3,  # Augmented
    DIMINISHED=4,  # Diminished
    DOMINANT=5,  # Dominant
    HALFDIM=6,  # Half-Diminished
    SUS4=7,  # Suspended-fourth
    MAJ6=8,  # Major-sixth
    MIN6=9,  # Minor-sixth
    MAJ7=10,  # Major-seventh
    MIN7=11,  # Minor-seventh
    AUG7=12,  # Augmented-seventh
    DIM7=13,  # Diminished-seventh
    MAJ9=14,  # Major-ninth
    MIN9=15,  # Minor-ninth
    DOM9=16,  # Dominant-ninth
    MIN11=17,  # Minor-eleventh
    DOM13=18,  # Dominant-thirteenth
    SUS2=19,  # Suspended-second
)


class Duration(object):
    val2name = {
        2.0: "BRV",
        1.0: "WHL",
        0.75: "DHLF",
        0.5: "HLF",
        0.375: "DQTR",
        0.25: "QTR",
        0.1875: "DEGT",
        0.125: "EGT",
        0.09375: "DSXT",
        0.0625: "SXT",
        0.046875: "DTSD",
        0.03125: "TSD",
        0.015625: "SXF",
    }
    name2val = {
        "BRV": 2.0,
        "WHL": 1.0,
        "DHLF": 0.75,
        "HLF": 0.5,
        "DQTR": 0.375,
        "QTR": 0.25,
        "DEGT": 0.1875,
        "EGT": 0.125,
        "DSXT": 0.09375,
        "SXT": 0.0625,
        "DTSD": 0.046875,
        "TSD": 0.03125,
        "SXF": 0.015625,
    }

    name2frac = {
        "BRV": "2",
        "WHL": "1",
        "DHLF": "3/4",
        "HLF": "1/2",
        "DQTR": "3/8",
        "QTR": "1/4",
        "DEGT": "3/16",
        "EGT": "1/8",
        "DSXT": "3/32",
        "SXT": "1/16",
        "DTSD": "3/64",
        "TSD": "1/32",
        "SXF": "1/64",
    }

    def __init__(self, d: float):
        self._val = d

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if Duration.valid_duration(self._val):
            return Duration.val2name[self._val]
        else:
            return f"{self._val:.4f}"

    def __add__(self, d: Duration) -> Duration:
        if isinstance(d, Duration):
            return Duration(self._val + d._val)
        elif isinstance(d, float):
            return Duration(self._val + d)
        else:
            raise RuntimeError(f"Cannot add duration and {type(d)}")

    def __sub__(self, d: Duration) -> Duration:
        if isinstance(d, Duration):
            return Duration(self._val - d._val)
        elif isinstance(d, float):
            return Duration(self._val - d)
        else:
            raise RuntimeError(f"Cannot add duration and {type(d)}")

    def __iadd__(self, d: Duration) -> Duration:
        return self.__add__(d)

    def __isub__(self, d: Duration) -> Duration:
        return self.__sub__(d)

    def __lt__(self, d: Duration):
        if isinstance(d, Duration):
            return self._val < d._val
        elif isinstance(d, float):
            return self._val < d
        else:
            raise RuntimeError(f"Cannot add duration and {type(d)}")

    def __eq__(self, d: Duration):
        if isinstance(d, Duration):
            return self._val == d._val
        elif isinstance(d, float):
            return self._val == d
        else:
            raise RuntimeError(f"Cannot add duration and {type(d)}")

    def __round__(self, ndigits=6):
        return round(self._val, ndigits)

    @staticmethod
    def valid_duration(v: float) -> None:
        return v in Duration.val2name


# Duration = enum(
#     BRV=2.0,  # Breve (Found in bach chorales)
#     WHL=1.0,  # whole note = one measure in 4/4
#     DHLF=0.75,  # dotted half
#     HLF=0.5,  # half note
#     DQTR=0.375,  # dotted quarter
#     QTR=0.25,  # quarter note
#     DEGT=0.1875,  # dotted eighth
#     EGT=0.125,  # eighth note
#     DSXT=0.09375,  # dotted sixteenth
#     SXT=0.0625,  # sixteenth note
#     DTSD=0.046875,  # dotted thirtysecond
#     TSD=0.03125,  # thirtysecond note
#     SXF=0.015625,  # sixty-fourth note
# )


HOLD = "__"
START = "START"
END = "END"

KEY_TYPE_MAP = {
    "major": KeyType.MAJOR,
    "minor": KeyType.MINOR,
    "major-minor": KeyType.MAJMIN,
    "augmented": KeyType.AUGMENTED,
    "diminished": KeyType.DIMINISHED,
    "dominant": KeyType.DOMINANT,
    "half-diminished": KeyType.HALFDIM,
    "suspended-fourth": KeyType.SUS4,
    "major-sixth": KeyType.MAJ6,
    "minor-sixth": KeyType.MIN6,
    "major-seventh": KeyType.MAJ7,
    "minor-seventh": KeyType.MIN7,
    "augmented-seventh": KeyType.AUG7,
    "diminished-seventh": KeyType.DIM7,
    "major-ninth": KeyType.MAJ9,
    "minor-ninth": KeyType.MIN9,
    "dominant-ninth": KeyType.DOM9,
    "minor-11th": KeyType.MIN11,
    "dominant-13th": KeyType.DOM13,
    "suspended-second": KeyType.SUS2,
    "none": KeyType.UNSET,
}

BASE_PITCH_MAP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

CHORD_SCALES = {
    KeyType.MAJOR: (0, 2, 4, 5, 7, 9, 11),
    KeyType.MINOR: (0, 2, 3, 5, 7, 8, 9, 10, 11),
    KeyType.AUGMENTED: (),
    KeyType.DIMINISHED: (0, 3, 6, 9),
    KeyType.DOMINANT: (0, 2, 4, 5, 7, 9, 10),
    KeyType.HALFDIM: (0, 3, 6, 10),
    KeyType.MAJMIN: (),
}

# NOTE: in some chords the notes will wraparound to the next octave
CHORD_TYPES = {
    KeyType.MAJOR: (0, 4, 7),
    KeyType.MINOR: (0, 3, 7),
    KeyType.AUGMENTED: (0, 4, 8),
    KeyType.DIMINISHED: (0, 3, 6),
    KeyType.DOMINANT: (0, 4, 7, 10),
    KeyType.HALFDIM: (0, 3, 6, 10),
    KeyType.MAJMIN: (0, 3, 7, 11),
    KeyType.SUS2: (0, 2, 7),
    KeyType.SUS4: (0, 5, 7),
    KeyType.MAJ6: (0, 4, 7, 9),
    KeyType.MIN6: (0, 3, 7, 9),
    KeyType.MAJ7: (0, 4, 7, 11),
    KeyType.MIN7: (0, 3, 7, 10),
    KeyType.AUG7: (0, 4, 8, 10),
    KeyType.DIM7: (0, 3, 6, 9),
    KeyType.MAJ9: (0, 4, 7, 11, 2),
    KeyType.MIN9: (0, 3, 7, 10, 2),
    KeyType.DOM9: (0, 4, 7, 10, 2),
    KeyType.MIN11: (0, 3, 7, 10, 2, 5),
    KeyType.DOM13: (0, 4, 7, 10, 2, 5, 9),
    KeyType.UNSET: (),
}


# =============================================================================
# Chord Scale Constants

MAJOR_VALUES = (0, 2, 4, 5, 7, 9, 11)
MINOR_VALUES = (0, 2, 3, 5, 7, 8, 9, 10, 11)
AUGMENTED_VALUES = ()
DIMINISHED_VALUES = (0, 3, 6, 9)
# NOTE: All of the above appear in triads

DOMINANT_VALUES = (0, 2, 4, 5, 7, 9, 10)
HALF_DIMINISHED_VALUES = (0, 3, 6, 10)
MINOR_MAJOR_VALUES = ()
AUGMENTED_MAJOR_VALUES = ()
# NOTE: All of the above appear in seventh chords
# =============================================================================


# =============================================================================
PENTATONIC_MINOR = (0, 3, 5, 7, 10)
PENTATONIC_MAJOR = (0, 2, 4, 7, 9)
BLUES_SCALE = (0, 3, 5, 6, 7, 10)
# =============================================================================


def get_pitch_val(pitch, octave=-1, alt=0):
    """
    :param pitch: [String] A single character representing the root pitch
    :param octave: [Integer] A numerical representation of the octave at which a pitch occurs
    :param alt: [Integer] Representation of a sharp or flat on a notes pitch
    :return: [Integer] a numerical representation of the pitch value in the range [0 - 11]
    """
    increase = (octave + 1) * 12
    offset = alt + BASE_PITCH_MAP[pitch]
    return int(increase + (offset % 12))


def assign_dur_label(num, denom):
    frac = float(num) / float(denom)
    if frac == 2.0:
        return Duration.BRV
    elif frac == 1.0:
        return Duration.WHL
    elif frac == 0.5:
        return Duration.HLF
    elif frac == 0.375:
        return Duration.DQTR
    elif frac == 0.25:
        return Duration.QTR
    elif frac == 0.1875:
        return Duration.DEGT
    elif frac == 0.125:
        return Duration.EGT
    elif frac == 0.09375:
        return Duration.DSXT
    elif frac == 0.0625:
        return Duration.SXT
    elif frac == 0.046875:
        return Duration.DTSD
    elif frac == 0.03125:
        return Duration.TSD
    elif frac == 0.015625:
        return Duration.SXF
    else:
        # NOTE: allows unrecognized durations to be returned
        return frac
