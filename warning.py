import yaml


def to_yaml(object):
    return yaml.dump(object)


def from_yaml(yaml_str):
    return yaml.safe_load(yaml_str)


yaml_str = to_yaml(
    {
        "layout": "post",
        "title": "Getting Started with Bandit",
        "date": "2017-01-16 10:00",
        "author": "Ian Cordasco",
    }
)
parsed_yaml = from_yaml(yaml_str)
