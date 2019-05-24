import models
import json
import datetime
import config


def test_populate_submission():
    filepath = \
        "data/cohort1/14/pre2-programming/20180724_152918"
    with open("tests/test_data/result_1.json", "r") as fp:
        result = json.load(fp)

    submisison = models.Submission().load(filepath, result)
    assert submisison.group_name == "cohort1"
    assert submisison.student_id == 14
    assert submisison.module_name == "pre2-programming"
    assert submisison.submission_date == \
        datetime.datetime.strptime(
            "20180724_152918",
            config.INPUT_DATE_FORMAT
        )
    for sf in submisison.submission_files:
        assert sf.filename.endswith(".py")
        # TODO: check score, breakdown scores
