import azure.functions as func
import json

from shared.file_helper import read_json, SUMMARY_FILE


def main(req: func.HttpRequest) -> func.HttpResponse:
    summary = read_json(SUMMARY_FILE, {})

    return func.HttpResponse(
        json.dumps(summary),
        status_code=200,
        mimetype="application/json"
    )