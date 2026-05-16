import azure.functions as func
import json
import re

from shared.file_helper import read_json, write_json, CANDIDATES_FILE

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()

        candidate_id = body.get("candidate_id")
        candidate_name = body.get("candidate_name")
        email = body.get("email")
        skills = body.get("skills")
        experience = body.get("experience")

        if not isinstance(candidate_id, int):
            return func.HttpResponse(
                json.dumps({"error": "Candidate ID must be an integer"}),
                status_code=400,
                mimetype="application/json"
            )

        if not isinstance(experience, int):
            return func.HttpResponse(
                json.dumps({"error": "Experience must be an integer"}),
                status_code=400,
                mimetype="application/json"
            )

        if not candidate_name:
            return func.HttpResponse(
                json.dumps({"error": "Candidate name is required"}),
                status_code=400,
                mimetype="application/json"
            )

        if not email or not re.match(EMAIL_REGEX, email):
            return func.HttpResponse(
                json.dumps({"error": "Invalid email format"}),
                status_code=400,
                mimetype="application/json"
            )

        if not isinstance(skills, list):
            return func.HttpResponse(
                json.dumps({"error": "Skills must be a list"}),
                status_code=400,
                mimetype="application/json"
            )

        candidates = read_json(CANDIDATES_FILE, [])

        duplicate = any(
            candidate["email"].lower() == email.lower()
            for candidate in candidates
        )

        if duplicate:
            return func.HttpResponse(
                json.dumps({"error": "Email already exists"}),
                status_code=400,
                mimetype="application/json"
            )

        new_candidate = {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "email": email,
            "skills": skills,
            "experience": experience
        }

        candidates.append(new_candidate)
        write_json(CANDIDATES_FILE, candidates)

        return func.HttpResponse(
            json.dumps({
                "message": "Candidate saved successfully",
                "candidate": new_candidate
            }),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON request body"}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )