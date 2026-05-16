import azure.functions as func
import logging

from shared.file_helper import (
    read_json,
    write_json,
    CANDIDATES_FILE,
    SUMMARY_FILE
)


def main(mytimer: func.TimerRequest) -> None:
    logging.info("Summary generation started")

    candidates = read_json(CANDIDATES_FILE, [])

    total = len(candidates)

    freshers = sum(
        1 for candidate in candidates
        if candidate["experience"] == 0
    )

    experienced = sum(
        1 for candidate in candidates
        if candidate["experience"] > 0
    )

    unique_skills = sorted(
        list({
            skill
            for candidate in candidates
            for skill in candidate["skills"]
        })
    )

    summary = {
        "total_applications": total,
        "freshers_count": freshers,
        "experienced_count": experienced,
        "unique_skills": unique_skills
    }

    write_json(SUMMARY_FILE, summary)

    logging.info("Summary generated successfully")