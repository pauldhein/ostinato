import pytest

from ostinato.siatec import siatec, TranslationalEquivalenceClass


def check_TECs(T):
    # TECs is a non-empty list of repeated patterns
    assert isinstance(T, list)
    assert len(T) > 0

    for tec in T:
        # TEC is a tuple with a defined pattern and a list of pattern offsets
        assert isinstance(tec, TranslationalEquivalenceClass)

        # Pattern must have at least two notes and there must be at least a
        # single translation
        assert len(tec.pattern) > 1
        assert len(tec.translators) > 0


def test_elbow_dataset(elbow_dataset):
    TECs = siatec(elbow_dataset)
    check_TECs(TECs)


def test_v_dataset(v_dataset):
    TECs = siatec(v_dataset)
    check_TECs(TECs)


def test_inv_elbow_dataset(inv_elbow_dataset):
    TECs = siatec(inv_elbow_dataset)
    check_TECs(TECs)


def test_retro_inv_dataset(retro_inv_dataset):
    TECs = siatec(retro_inv_dataset)
    check_TECs(TECs)

    # ================================================


def test_mid_inv_elbow_dataset(mid_inv_elbow_dataset):
    TECs = siatec(mid_inv_elbow_dataset)
    check_TECs(TECs)


def test_regular_dataset(regular_dataset):
    TECs = siatec(regular_dataset)
    check_TECs(TECs)


def test_retro_dataset(retro_dataset):
    TECs = siatec(retro_dataset)
    check_TECs(TECs)


def test_repeated_retro_dataset(repeated_retro_dataset):
    TECs = siatec(repeated_retro_dataset)
    check_TECs(TECs)


def test_odd_retro_dataset(odd_retro_dataset):
    TECs = siatec(odd_retro_dataset)
    check_TECs(TECs)


def test_separated_retro_dataset(separated_retro_dataset):
    TECs = siatec(separated_retro_dataset)
    check_TECs(TECs)


def test_middle_retro_dataset(middle_retro_dataset):
    TECs = siatec(middle_retro_dataset)
    check_TECs(TECs)


def test_shifted_retro_dataset(shifted_retro_dataset):
    TECs = siatec(shifted_retro_dataset)
    check_TECs(TECs)


def test_big_shifted_retro_dataset(big_shifted_retro_dataset):
    TECs = siatec(big_shifted_retro_dataset)
    check_TECs(TECs)


def test_geometric_data(geometric_data):
    TECs = siatec(geometric_data)
    check_TECs(TECs)
