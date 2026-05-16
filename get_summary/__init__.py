import azure.functions as func

import json

import os
 
def main(req: func.HttpRequest) -> func.HttpResponse:

    file_path = "data/summary.json"
 
    default_summary = {

        "total_applications": 0,

        "freshers_count": 0,

        "experienced_count": 0,

        "unique_skills": []

    }
 
    try:

        if os.path.exists(file_path):

            with open(file_path, "r") as f:

                data = json.load(f)

                return func.HttpResponse(

                    json.dumps(data),

                    mimetype="application/json",

                    status_code=200

                )
 
        return func.HttpResponse(

            json.dumps(default_summary),

            mimetype="application/json",

            status_code=200

        )
 
    except Exception as e:

        return func.HttpResponse(str(e), status_code=500)
 