from typing import Dict, Any
import yaml

def load_config(path_config: str) -> Dict[str, Any]:
    """
    Read yaml config.

    Args:
        path_config (str): path to yaml config

    Returns:
        Dict[str, Any]: config values
    """
    with open(path_config, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config