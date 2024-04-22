#!/usr/bin/env python
import argparse
import logging
import os
import requests
from domino import Domino


def parse_args():
    parser = argparse.ArgumentParser(description="A script to publish Domino Models")
    parser.add_argument(
        "DOMINO_JOB_OP", type=str, help="Operation: create, list, or update."
    )
    parser.add_argument("DOMINO_PROJECT_OWNER", type=str, help="Domino Project Owner.")
    parser.add_argument("DOMINO_PROJECT_NAME", type=str, help="Domino Project Name.")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")
    parser.add_argument(
        "DOMINO_API_HOST",
        type=str,
        help="Domino URL for external or http://nucleus-frontend.domino-platform:80 from a workspace.",
    )
    parser.add_argument(
        "DOMINO_JOB_COMMAND",
        type=str,
        help="Command to run for the job. Command format: 'main.py arg1 arg2'.",
    )
    parser.add_argument("DOMINO_JOB_ID", type=str, help="JOB ID to stop the Job.")
    parser.add_argument(
        "DOMINO_JOB_COMMIT_ID", type=str, help="Commit Id of the project."
    )
    parser.add_argument(
        "DOMINO_JOB_HARDWARE_TIER_NAME", type=str, help="Job Hardware Tier Name."
    )
    parser.add_argument(
        "DOMINO_JOB_ENVIRONMENT_ID", type=str, help="Environment Id of the Job."
    )
    return parser.parse_args()


def get_owner_id(domino_url, user_api_key):
    logging.info(f"Getting Owner Id for the api key {user_api_key}")
    url = f"https://{domino_url}/v4/users/self"
    headers = {"X-Domino-Api-Key": user_api_key}
    response = requests.get(url, headers=headers)
    return response.json()


def get_project_id(domino_url, project_name, user_api_key):
    owner_id = get_owner_id(domino_url, user_api_key).get("id")
    logging.info(f"Getting project id for owner id: {owner_id}")
    url = f"https://{domino_url}/v4/projects"
    params = {"name": project_name, "ownerId": owner_id}
    headers = {"X-Domino-Api-Key": user_api_key}
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_hardware_tier_id(domino_url, user_api_key, hardware_tier_name):
    owner_id = get_owner_id(domino_url, user_api_key).get("id")
    logging.info(f"Getting hardware tier id for owner id: {owner_id}")
    url = f"https://{domino_url}/v4/hardwareTier"
    headers = {"X-Domino-Api-Key": user_api_key}
    hardware_tier_list = requests.get(url, headers=headers).json()
    tier_id = next(
        (
            tier["id"]
            for tier in hardware_tier_list
            if tier["name"] == hardware_tier_name
        ),
        None,
    )
    return tier_id


def job_start(
    domino,
    command,
    hardware_tier_id,
    environment_id,
):

    response = domino.jobstart(
        command,
        hardware_tier_name=hardware_tier_id,
        environment_id=environment_id,
    )
    print("job id :: ", response.id)


def job_stop(domino, job_id):
    domino.job_stop(job_id)


def main():
    inputs = parse_args()
    logging.info(inputs.DOMINO_PROJECT_NAME)
    logging.info(inputs.DOMINO_USER_API_KEY)
    logging.info(inputs.DOMINO_API_HOST)
    domino_url = inputs.DOMINO_API_HOST

    project = f"{inputs.DOMINO_PROJECT_OWNER}/{inputs.DOMINO_PROJECT_NAME}"
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )

    if inputs.DOMINO_JOB_OP == "start":
        job_start(
            domino,
            inputs.DOMINO_JOB_COMMAND,
            get_hardware_tier_id(
                domino_url,
                inputs.DOMINO_USER_API_KEY,
                inputs.DOMINO_JOB_HARDWARE_TIER_NAME,
            ),
            inputs.DOMINO_JOB_ENVIRONMENT_ID,
        )
    elif inputs.DOMINO_JOB_OP == "stop":
        job_stop(domino, inputs.DOMINO_JOB_ID)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
