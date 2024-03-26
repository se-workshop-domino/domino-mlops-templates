#!/usr/bin/env python
import argparse
import logging
from domino import Domino


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="A script to publish Domino Apps")
    parser.add_argument("DOMINO_PROJECT_OWNER", type=str, help="Domino Project Owner.")
    parser.add_argument("DOMINO_PROJECT_NAME", type=str, help="Domino Project Name.")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")
    parser.add_argument(
        "DOMINO_API_HOST",
        type=str,
        help="Domino URL for external or http://nucleus-frontend.domino-platform:80 from a workspace.",
    )
    parser.add_argument(
        "DOMINO_HARDWARE_TIER_ID", type=str, help="Domino hardware tier for the app"
    )
    args = parser.parse_args()
    return args


def app_publish(domino, hardwareTierId=None):
    """
    Publish a brand new app.

    Args:
        domino (Domino): Domino object.
        hardwareTierId (str): Hardware tier ID.
    """

    response = domino.app_publish(
        unpublishRunningApps=True, hardwareTierId=hardwareTierId
    )

    if response.status_code == 200:
        logging.info(f"{response.status_code}: {response.reason}")


def app_unpublish(domino):
    """
    Unpublish app.

    Args:
        domino (Domino): Domino object.
    """
    # Unpublish app
    response = domino.app_unpublish()

    if response.status_code == 200:
        logging.info(f"{response.status_code}: {response.reason}")


def main():
    """
    Main function to execute the script.
    """
    inputs = parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    logging.info(inputs.DOMINO_PROJECT_NAME)
    logging.info(inputs.DOMINO_USER_API_KEY)
    logging.info(inputs.DOMINO_API_HOST)

    project = f"{inputs.DOMINO_PROJECT_OWNER}/{inputs.DOMINO_PROJECT_NAME}"
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )

    if inputs.DOMINO_MODEL_OP == "publish":
        app_publish(domino, inputs.DOMINO_HARDWARE_TIER_ID)
    elif inputs.DOMINO_MODEL_OP == "unpublish":
        app_unpublish(domino)


if __name__ == "__main__":
    main()
