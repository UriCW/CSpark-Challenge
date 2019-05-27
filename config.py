# CONNECTION_STRING = 'mongodb://root:example@localhost:27017/submissions' + \
CONNECTION_STRING = 'mongodb://root:example@mongo:27017/submissions' + \
    '?authSource=admin'
MOCK_CONNECTION_STRING = 'mongodb://root:example@localhost:27017/mock_submissions'
INPUT_DATE_FORMAT = "%Y%m%d_%H%M%S"
RESULTS_FILENAME = "results.json"
DATABASE_POPULATED_LOCK_FILE = "/var/lock/teacher-dashboard-populated.lock"
DATAFILES_PATH = "./data"


class DevelopmentConfig(object):
    MONGODB_SETTINGS = {
        "host": CONNECTION_STRING,
        "db": "submission"
    }
