import argparse
import config
# from os import walk, path
import os
import logging
from models import Submission
import json
from mongoengine import connect


def populate(connection_string, root_path, ignore_lock=False):
    """ Populates database with submission objects

    :connection_string:
    :root_path:
    :return: list of Submission models
    """
    ret = []

    # Check is not populated alread
    if not ignore_lock and os.path.exists(config.DATABASE_POPULATED_LOCK_FILE):
        logging.info(
            "Database lock file {} exists, will not seed database"
            .format(config.DATABASE_POPULATED_LOCK_FILE)
        )
        return

    for (path, directories, files) in os.walk(root_path):
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
    # Create lockfile
    open(config.DATABASE_POPULATED_LOCK_FILE, "w").close()
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
