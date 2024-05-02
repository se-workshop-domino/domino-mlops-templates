import configparser
import argparse

def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="A script to publish Domino Apps")
    parser.add_argument("DOMINO_ENV", type=str, help="Domino Environment")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")

    args = parser.parse_args()
    return args


def read_config(section, key):
   config = configparser.ConfigParser()
   config.read('./env-variables.ini')
   print(config.sections()) 
   return config[section][key]



def parse_evn_var(env_variables,section):

    env_variables.DOMINO_PROJECT_OWNER = read_config(section, "DOMINO_PROJECT_OWNER")
    env_variables.DOMINO_PROJECT_NAME = read_config(section, "DOMINO_PROJECT_NAME")
    env_variables.DOMINO_API_HOST = read_config(section, "DOMINO_API_HOST")
    env_variables.DOMINO_MODEL_OP = read_config(section, "DOMINO_MODEL_OP")
    env_variables.DOMINO_MODEL_NAME = read_config(section, "DOMINO_MODEL_NAME")
    env_variables.DOMINO_MODEL_DESC = read_config(section, "DOMINO_MODEL_DESC")
    env_variables.DOMINO_MODEL_FILE = read_config(section, "DOMINO_MODEL_FILE")
    env_variables.DOMINO_MODEL_FUNC = read_config(section, "DOMINO_MODEL_FUNC")
    env_variables.DOMINO_MODEL_CE = read_config(section, "DOMINO_MODEL_CE")
    env_variables.DOMINO_HARDWARE_TIER_NAME = read_config(section, "DOMINO_HARDWARE_TIER_NAME")
    env_variables.DOMINO_ENVIRONMENT_ID = read_config(section, "DOMINO_ENVIRONMENT_ID")
    env_variables.DOMINO_REGISTERED_MODEL_NAME = read_config(section, "DOMINO_REGISTERED_MODEL_NAME")
    env_variables.DOMINO_REGISTERED_MODEL_VERSION = read_config(section, "DOMINO_REGISTERED_MODEL_VERSION")
    env_variables.DOMINO_MODEL_TYPE = read_config(section, "DOMINO_MODEL_TYPE")
    env_variables.DOMINO_TARGET_STAGE = read_config(section, "DOMINO_TARGET_STAGE")
    env_variables.DOMINO_REVIEWER = read_config(section, "DOMINO_REVIEWER")

    return env_variables
