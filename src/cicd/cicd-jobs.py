#!/usr/bin/env python
import argparse
import logging
import os
import requests


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
    headers = {"Authorization": f"Bearer {user_api_key}"}
    response = requests.get(url, headers=headers)
    return response.json()


def get_project_id(domino_url, project_name, user_api_key):
    owner_id = get_owner_id(domino_url, user_api_key).get("id")
    logging.info(f"Getting project id for owner id: {owner_id}")
    url = f"https://{domino_url}/v4/projects"
    params = {"name": project_name, "ownerId": owner_id}
    headers = {"Authorization": f"Bearer {user_api_key}"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_hardware_tier_id(domino_url, user_api_key, hardware_tier_name):
    owner_id = get_owner_id(domino_url, user_api_key).get("id")
    logging.info(f"Getting hardware tier id for owner id: {owner_id}")
    url = f"https://{domino_url}/v4/hardwareTier"
    headers = {"Authorization": f"Bearer {user_api_key}"}
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
    start_job_url,
    project_id,
    command,
    commit_id,
    hardware_tier_name,
    environment_id,
    user_api_key,
):
    payload = {
        "projectId": project_id,
        "runCommand": command,
        "mainRepoGitRef": {"refType": "branches", "value": commit_id},
        "overrideHardwareTierId": get_hardware_tier_id(hardware_tier_name),
    }
    headers = {"Authorization": f"Bearer {user_api_key}"}
    response = requests.post(start_job_url, headers=headers, json=payload)
    print(response.text)


def job_stop(stop_job_url, project_id, job_id, user_api_key):
    payload = {"projectId": project_id, "jobId": job_id}
    headers = {"Authorization": f"Bearer {user_api_key}"}
    response = requests.post(stop_job_url, headers=headers, json=payload)
    print(response.text)


def main():
    inputs = parse_args()
    logging.info(inputs.DOMINO_PROJECT_NAME)
    logging.info(inputs.DOMINO_USER_API_KEY)
    logging.info(inputs.DOMINO_API_HOST)
    start_job_url = f"https://{inputs.DOMINO_API_HOST}/v4/jobs/start"
    stop_job_url = f"https://{inputs.DOMINO_API_HOST}/v4/jobs/stop"
    project_name = f"{inputs.DOMINO_PROJECT_OWNER}/{inputs.DOMINO_PROJECT_NAME}"
    project_id = get_project_id(
        inputs.DOMINO_API_HOST, project_name, inputs.DOMINO_USER_API_KEY
    )

    if inputs.DOMINO_JOB_OP == "start":
        job_start(
            start_job_url,
            project_id,
            inputs.DOMINO_JOB_COMMAND,
            inputs.DOMINO_JOB_COMMIT_ID,
            inputs.DOMINO_JOB_HARDWARE_TIER_NAME,
            inputs.DOMINO_JOB_ENVIRONMENT_ID,
            inputs.DOMINO_USER_API_KEY,
        )
    elif inputs.DOMINO_JOB_OP == "stop":
        job_stop(
            stop_job_url, project_id, inputs.DOMINO_JOB_ID, inputs.DOMINO_USER_API_KEY
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
