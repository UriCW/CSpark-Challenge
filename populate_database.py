import argparse
import config
from os import walk
import logging
from models import Submission
import json
from mongoengine import connect


def populate(connection_string, root_path):
    """ Populates database with submission objects

    :connection_string:
    :root_path:
    :return: list of Submission models
    """
    ret = []
    for (path, directories, files) in walk(root_path):
        if not files:
            continue
        if files == [config.RESULTS_FILENAME]:
            group, student_id, module, submission_date = path.split("/")[-4:]
            fn = path + "/" + files[0]
            with open(fn, "r") as fp:
                results = json.load(fp)
            submission = Submission().load(path, results)
            ret.append(submission)
        else:
            msg = "Unexpected files {} found in directory {}".format(
                files,
                path
            )
            logging.warning(msg)
    connect(host=connection_string)
    for submission in ret:
        submission.save()
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populates a mongodb database"
    )
    parser.add_argument(
        "root_path",
        help="The root data directory"
    )
    parser.add_argument(
        "--connection-string",
            default=config.CONNECTION_STRING,
            help="Database connection string"
    )
    args = parser.parse_args()
    models = populate(args.connection_string, args.root_path)
