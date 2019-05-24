CONNECTION_STRING = 'mongodb://root:example@localhost:27017/submissions' + \
    '?authSource=admin'
MOCK_CONNECTION_STRING = 'mongodb://root:example@localhost:27017/mock_submissions'
INPUT_DATE_FORMAT = "%Y%m%d_%H%M%S"
RESULTS_FILENAME = "results.json"


class DevelopmentConfig(object):
    MONGODB_SETTINGS = {
        # "host": "mongodb://root:example@localhost:27017/submissions",
        "host": CONNECTION_STRING,
        "db": "submission"
    }
