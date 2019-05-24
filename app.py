from flask import Flask, request, render_template, jsonify
from flask_mongoengine import MongoEngine
import config
import models
import pipelines
app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = MongoEngine(app)


@app.route("/groups")
def groups():
    """ Gets a list of all group names

    :return: a list of group names
    """
    groups = models.Submission.objects().distinct("group_name")
    return jsonify(groups)


@app.route("/data/top_scores")
def top_scores():
    """ Gets a list of results, one for each student/module
    [
        {
         'group':<GROUP>,
         'student':<STUDENT>,
         'module':<MODULE>,
         'score':<SCORE>
        },
        ...
    ]
    """
    pipeline = pipelines.top_scores
    dataset = models.Submission.objects().aggregate(*pipeline)
    ret = []
    for d in dataset:
        ret.append(d)
    return jsonify(ret)


@app.route("/graph/grades")
def grades():
    """ Returns a data object to display bar chart with
    """
    ret = {
        'labels': [],
        'datasets': [],
    }

    groups = request.args.getlist(
        'group') or models.Submission.objects().distinct("group_name")
    modules = sorted(models.Submission.objects().distinct("module_name"))
    for m in modules:
        ret['datasets'].append({"label": m, "data": []})
    students = sorted(models.Submission.objects(
        group_name__in=groups).distinct("student_id"))
    ret['labels'] = students

    for s in students:
        for m in modules:
            objs = models.Submission.objects(student_id=s, module_name=m)
            result = objs.order_by("-submission_date").limit(-1).first()
            if not result:
                result = 0
            else:
                result = result['submission_score']

            for ds in ret['datasets']:
                if ds['label'] == m:
                    ds['data'].append(result)
            # print("{} - {} - {}".format(s, m, result))
        # print()
    # print(ret)
    return jsonify(ret)


@app.route("/graph/distributions")
def distributions():
    ret = {}
    groups = request.args.getlist(
        'group') or models.Submission.objects().distinct("group_name")

    ranges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    last = 0
    for r in ranges:
        label = "{} to {}".format(last, r)
        count = models.Submission.objects(
        ).count()
        print(count)
        last = r
    return jsonify(ret)


@app.route("/graph/resubmissions")
def resumbissions():
    """ Gets the datasets for scatter plot of resubmission improvements
    """
    groups = request.args.getlist(
        'group') or models.Submission.objects().distinct("group_name")
    pipeline = pipelines.submission_scatter
    datasets = models.Submission.objects(
        group_name__in=groups).aggregate(*pipeline)
    ret = []
    for d in datasets:
        ret.append(d)
    return jsonify(ret)


#@app.route("/")
@app.route("/submissions")
def root():
    groups = request.args.getlist(
        'group') or models.Submission.objects().distinct("group_name")
    return render_template("scat.html")


@app.route("/")
@app.route("/results")
def results():
    groups = request.args.getlist(
        'group') or models.Submission.objects().distinct("group_name")
    return render_template("results.html")

if __name__ == "__main__":
    app.run()
