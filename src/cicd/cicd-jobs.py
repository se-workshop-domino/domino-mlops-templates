#!/usr/bin/env python
import argparse,os
from domino import Domino

def parse_args():
    parser=argparse.ArgumentParser(description="a script to publish Domino Models")
    parser.add_argument("DOMINO_JOB_OP", type=str, help="create, list or update.")
    parser.add_argument("DOMINO_PROJECT_OWNER", type=str, help="Domino Project Owner.")
    parser.add_argument("DOMINO_PROJECT_NAME", type=str, help="Domino Project Name.")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")
    parser.add_argument("DOMINO_API_HOST", type=str, help="Domino URL for external or http://nucleus-frontend.domino-platform:80 from a workspace.")
    parser.add_argument("DOMINO_JOB_COMMAND", type=str, help="Command to run for the job command='main.py arg1 arg2'.")
    parser.add_argument("DOMINO_JOB_ID", type=str, help="JOB ID to stop the Job")
    parser.add_argument("DOMINO_JOB_COMMIT_ID", type=str, help="Commit Id of the project.")
    parser.add_argument("DOMINO_JOB_HARDWARE_TIER_NAME", type=str, help="Job Hardware Tier Name.")
    parser.add_argument("DOMINO_JOB_ENVIRONMENT_ID", type=str, help="Enviornment Id of the Job.")
    args=parser.parse_args()
    return args

def list_environments(domino):
    all_available_environments = domino.environments_list()
    global_environments = list(
        filter(
            lambda x: x.get("visibility") == "Global", all_available_environments["data"]
        )
    )
    print(
        "This Domino deployment has \
         {} global environments".format(
            len(global_environments)
        )
    )
    
def list_jobs(domino):
    #print(f"{domino.models_list()}")
    pass
    
def job_start(domino, command, commit_id,hardware_tier_name,environment_id):
    models = domino.job_start(        
        command = command,
        commit_id = commit_id,
        hardware_tier_name = hardware_tier_name,
        environment_id = environment_id
        )
    
def job_stop(domino, job_id):
    models = domino.job_stop(        
        domino,job_id
        )    
    
def main():
    inputs=parse_args()
    print(inputs.DOMINO_MODEL_NAME)
    print(inputs.DOMINO_PROJECT_NAME)
    print(inputs.DOMINO_USER_API_KEY)
    print(inputs.DOMINO_API_HOST)

    project=  inputs.DOMINO_PROJECT_OWNER + "/" + inputs.DOMINO_PROJECT_NAME
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )

    if inputs.DOMINO_JOB_OP == "start":
        job_start(domino,inputs.DOMINO_JOB_COMMAND, inputs.DOMINO_JOB_COMMIT_ID, inputs.DOMINO_JOB_HARDWARE_TIER_NAME, inputs.DOMINO_JOB_ENVIRONMENT_ID)
    elif inputs.DOMINO_JOB_OP == "stop":
        job_stop(domino,inputs.DOMINO_JOB_ID)

if __name__ == '__main__':
    main()