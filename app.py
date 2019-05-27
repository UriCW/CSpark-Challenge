from flask import Flask, request, render_template, jsonify
from flask_mongoengine import MongoEngine
import config
import models
import pipelines
import populate_database

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


@app.route("/students")
def students():
    """ Gets a list of student IDs

    optionally limit to students in groups
    using the group URL parameter

    :group: group name to include, default to all,
        accepts multiple occurances
    :return: a list of student IDs
    """
    all_groups = models.Submission.objects().distinct("group_name")
    groups = request.args.getlist('group') or all_groups

    students = models.Submission.objects(
        group_name__in=groups
    ).distinct("student_id")
    return jsonify(students)


@app.route("/data/top_scores")
def top_scores():
    """ Gets a list of results, one for each student/module

    :return: a list of result entries in the format
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
def grades_graph_api():
    """ Returns a data object to display results bar chart with
    """
    ret = {
        'labels': [],
        'datasets': [],
    }

    all_groups = models.Submission.objects().distinct("group_name")
    groups = request.args.getlist('group') or all_groups

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
    return jsonify(ret)


@app.route("/graph/histogram")
def distribution_graph_api():
    """ Gets the grade histogram data, count occurances of each score range
        for each module
    """
    ranges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ret = {
        'labels': ranges,
        'datasets': []
    }
    all_groups = models.Submission.objects().distinct("group_name")
    groups = request.args.getlist('group') or all_groups
    pipeline = pipelines.top_scores

    modules = models.Submission.objects().distinct("module_name")
    for m in modules:
        # Iterator can't be reset, so recreate each time
        datasets = models.Submission.objects(
            group_name__in=groups
        ).aggregate(*pipeline)

        # Get a list of scores for module m
        dataset = {'label': m, 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        scores = [e['score'] for e in datasets if e['module'] == m]

        # Count occurances of score ranges
        lower_limit = 0
        for idx, upper_limit in enumerate(ranges):
            num_scores_in_range = len(
                [s for s in scores if s > lower_limit and s <= upper_limit]
            )
            dataset['data'][idx] = num_scores_in_range
            lower_limit = upper_limit
        ret['datasets'].append(dataset)
    return jsonify(ret)


@app.route("/graph/resubmissions")
def resumbissions_graph_api():
    """ Gets the datasets for scatter plot of resubmission improvements
    """
    all_groups = models.Submission.objects().distinct("group_name")
    groups = request.args.getlist('group') or all_groups

    pipeline = pipelines.submission_scatter
    datasets = models.Submission.objects(
        group_name__in=groups
    ).aggregate(*pipeline)
    ret = []
    for d in datasets:
        ret.append(d)
    return jsonify(ret)


@app.route("/graph/student/<int:student_id>")
def student_graph_api(student_id):
    pipeline = pipelines.submission_scatter
    datasets = models.Submission.objects(
        student_id=student_id
    ).aggregate(*pipeline)
    ret = [d for d in datasets]
    return jsonify(ret)


@app.route("/")
@app.route("/submissions")
def root():
    return render_template("scat.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/student/<int:student_id>")
def student(student_id):
    return render_template("student.html", student=student_id)
    # return render_template("student.html", student=student_id)


@app.route("/histogram")
def histogram():
    return render_template("histogram.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
