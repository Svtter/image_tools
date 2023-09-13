"""change pypi"""

import tomli
import tomli_w
from pathlib import Path

conf_map = {
    "thinghoo": """[global]
index = http://nexus.beijing-epoch.com/repository/pypi-thinghoo-group/pypi
index-url = http://nexus.beijing-epoch.com/repository/pypi-thinghoo-group/simple
""",
    "tsinghua": """[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
""",
}

toml_map = {
    "thinghoo": "http://nexus.beijing-epoch.com/repository/pypi-thinghoo-group/simple",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple",
}


def replace_pypi_in_toml_file(name: str):
    """name: pypi mirror name"""
    p = Path("pyproject.toml")
    if not p.exists():
        print("no `pyproject.toml` file.")
        return

    # parse toml file
    # find specific section in toml content
    toml_data = p.read_text()
    toml_dict = tomli.loads(toml_data)

    mirror_url = toml_map[name]

    # find the [[tool.poetry.source]] section, in pyproject.toml file.
    toml_dict["tool"]["poetry"]["source"] = {
        "name": name,
        "url": mirror_url,
        "default": True,
    }

    # write back
    p.write_text(tomli_w.dumps(toml_dict))


def set_pypi(conf):
    if not conf:
        return

    if not conf in conf_map.keys():
        print('conf must be one of ["thinghoo", "tsinghua"]')
        return

    content = conf_map[conf]
    with open(Path.home().joinpath(".config/pip/pip.conf"), "w") as f:
        f.write(content)
    replace_pypi_in_toml_file(conf)

    print("pypi set done.")
