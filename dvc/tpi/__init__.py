import json
import logging
import os
from collections import OrderedDict

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
TEMPLATE_MAIN = "main.tf"

BASE_CONFIG = {
    "//": "This file auto-generated by dvc-tpi, do not edit manually.",
    "terraform": {
        "required_providers": {
            "iterative": {
                "source": "iterative/iterative",
            },
        },
    },
    "provider": {
        "iterative": {},
    },
}

_jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)


def render_config(**config) -> str:
    """Render TPI iterative_machine config as terraform HCL."""
    assert "name" in config and "cloud" in config
    template = _jinja_env.get_template(TEMPLATE_MAIN)
    return template.render(**config)


def render_json(indent=None, **config) -> str:
    """Render TPI iterative_machine config as terraform JSON."""
    assert "name" in config and "cloud" in config
    tf_config = OrderedDict(BASE_CONFIG)
    name = config["name"]
    resource = {
        name: {key: value for key, value in config.items()},
    }
    tf_config["resource"] = {"iterative_machine": resource}
    return json.dumps(tf_config, indent=indent)
