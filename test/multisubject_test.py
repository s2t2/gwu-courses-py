

from app.multisubject import csv_to_list


def test_subject_ids_parser():
    assert csv_to_list("") == []
    assert csv_to_list("CSCI") == ["CSCI"]
    assert csv_to_list("CSCI,EMSE") == ["CSCI", "EMSE"]
    assert csv_to_list("CSCI,   EMSE,ISTM, OOPS") == ["CSCI", "EMSE", "ISTM", "OOPS"]
