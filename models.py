from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField
from mongoengine.fields import StringField, IntField, FloatField, DateTimeField, EmbeddedDocumentField
import datetime
import config


class ScoreBreakdown(EmbeddedDocument):
    unittest = FloatField()
    pep8 = FloatField()
    pylint = FloatField()

    def __init__(self, score_breakdown):
        """ Populate ScoreBreakdown

        :score_breakdown: A dictionary with keys:
            "Unittest",
            "Pep8",
            "Pylint"
        """
        # EmbeddedDocument.__init__(self)
        super(ScoreBreakdown, self).__init__()
        self.unittest = score_breakdown['Unittest']
        self.pep8 = score_breakdown['Pep8']
        self.pylint = score_breakdown['Pylint']


class SubmissionFile(EmbeddedDocument):
    filename = StringField(required=True)
    score = FloatField()
    breakdown = EmbeddedDocumentField(ScoreBreakdown)

    def __init__(self, filestats):
        """ Populate a SubmissionFile

        :filestats: A dictionary containing keys:
            "file": filename
            "file_score": score
            "score_per_metric": ScoreBreakdown dictionary
        """
        super(SubmissionFile, self).__init__()
        # EmbeddedDocument.__init__(self)
        self.filename = filestats['file']
        self.score = filestats['file_score']
        self.breakdown = ScoreBreakdown(filestats['score_per_metric'])


class Submission(Document):
    group_name = StringField(required=True)
    student_id = IntField(required=True)
    module_name = StringField(required=True)
    submission_date = DateTimeField(required=True)
    submission_files = EmbeddedDocumentListField(SubmissionFile)
    submission_score = FloatField(required=True)

    def __init__(self, filepath, results):
        """ Initiate a new Submission entry

        :filepath: A fileparth ending in
            "group_name/student_id/module_name/submission_date'
            e.g. data/cohort1/14/pre2-programming/20180724_152918/
        :results: A dictionary populated by the contents of results.json in filepath
        """
        # Document.__init__(self)
        super(Submission, self).__init__()
        # Populated from filepath
        group, student, module, time = filepath.split("/")[-4:]
        self.group_name = group
        self.student_id = int(student)
        self.module_name = module
        self.submission_date = datetime.datetime.strptime(
            time,
            config.INPUT_DATE_FORMAT
        )
        # Populated from json (results.json)
        self.submission_score = results["overall_score"]
        for filestats in results["data"]:
            self.submission_files.append(SubmissionFile(filestats))
