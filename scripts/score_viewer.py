import argparse
import logging

from ostinato.music_elements import Score
from ostinato.siatec import siatec


def main(args):
    logger = logging.getLogger("music-element-logger")
    logger.setLevel("DEBUG")
    xml_filepath = args.filepath
    score = Score.from_xml_file(xml_filepath)
    print(score)

    part_num = 1
    dataset = score.to_siatec_score(part_num)
    # print(dataset)
    TECs = siatec(dataset)
    min_patt_size = 3
    min_num_patts = 1
    decent_TECs = sorted(
        [
            tec
            for tec in TECs
            if len(tec.pattern) >= min_patt_size
            and len(tec.translators) >= min_num_patts
        ],
        key=lambda tec: (len(tec.pattern), len(tec.translators)),
        reverse=True,
    )

    for i, tec in enumerate(decent_TECs):
        print(f"TEC #{i+1}:\n{tec}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Musical score viewer",
        description="Given a path to a MusicXML file, this script will parse the file and display a textual representation of the musical score found in the file.",
    )
    parser.add_argument(
        "filepath",
        help="Path to a MusicXML file that ends either in .xml or .mxl",
    )
    args = parser.parse_args()
    main(args)
