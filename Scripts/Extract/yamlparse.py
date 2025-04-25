import yaml
import os



# parsing yaml file
def parse_yaml(yaml_path):
    """
    Parse a YAML file and return the data as a dictionary.
    """
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data



