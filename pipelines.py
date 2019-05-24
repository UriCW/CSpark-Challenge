# Note:
# I'm aware this isn't PEP8 compliant, but these aren't functions.
# Not sure what's the correct commenting style for this is


# submission score over date, grouped by student_id and module_name:
# returns:
# [
#   {
#       "label": "Student_<STUDENT_ID>_<MODULE>",
#       "data": [ {"x": <DATE_STRING>, "y": <SUBMISSION_SCORE>}, ...],
#       "student": <STUDENT_ID>,
#   }, ...
# ]
submission_scatter = [
    {"$group":
        {
            "_id": {"student": "$student_id", "module": "$module_name"},
            "data": {"$push": {"x": {"$dateToString": {"date": "$submission_date"}}, "y": "$submission_score"}},
        }
     },
    {"$project":
        {
            "_id": 0,
            "label": {"$concat": ["Student_", {"$toString": "$_id.student"}, "_", "$_id.module"]},
            "data": 1,
            "student": "$_id.student",
        }
     },
]

# Gets only the top score for each student:
# returns:
# [
#  {'group':<GROUP>, 'student':<STUDENT>, 'module':<MODULE>, 'score':<SCORE>},
#  ...
# ]
top_scores = [
    {
        '$group': {
            "_id": {
                "group": "$group_name",
                    "student": "$student_id",
                    "module": "$module_name",
            },
                "score": {"$max": "$submission_score"},
        }
    },
    {
        '$sort': {
            "_id.group": 1,
            "_id.student": 1,
            "_id.module": 1,

        }
    },
    {
        '$project': {
            "_id": 0,
            "group": "$_id.group",
            "student": "$_id.student",
            "module": "$_id.module",
            "score": "$score",
        }
    },
]
