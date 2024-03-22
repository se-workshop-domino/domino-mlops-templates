#!/usr/bin/env python
import argparse,os
from domino import Domino

def parse_args():
    parser=argparse.ArgumentParser(description="a script to publish Domino Apps")
    parser.add_argument("DOMINO_PROJECT_OWNER", type=str, help="Domino Project Owner.")
    parser.add_argument("DOMINO_PROJECT_NAME", type=str, help="Domino Project Name.")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")
    parser.add_argument("DOMINO_API_HOST", type=str, help="Domino URL for external or http://nucleus-frontend.domino-platform:80 from a workspace.")
    parser.add_argument("DOMINO_HARDWARE_TIER", type=str, help="Domino hardware tier for the app")
    args=parser.parse_args()
    return args

def app_publish(domino,unpublishRunningApps=True, hardwareTierId=None):
    # Publish a brand new app
    response = domino.app_publish(unpublishRunningApps, hardwareTierId)

    if response.status_code == 200:
        print(f"{response.status_code}: {response.reason}")


    
def app_unpublish(domino):
    # Un Publlish app
    response = domino.app_unpublish()

    if response.status_code == 200:
        print(f"{response.status_code}: {response.reason}")
    
def main():
    inputs=parse_args()
    print(inputs.DOMINO_PROJECT_NAME)
    print(inputs.DOMINO_USER_API_KEY)
    print(inputs.DOMINO_API_HOST)

    project=  inputs.DOMINO_PROJECT_OWNER + "/" + inputs.DOMINO_PROJECT_NAME
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )
    if inputs.DOMINO_MODEL_OP == "publish":
        app_publish(domino, inputs.DOMINO_HARDWARE_TIER)
    elif inputs.DOMINO_MODEL_OP == "unpublish":
        app_unpublish(domino) 
        

if __name__ == '__main__':
    main()

