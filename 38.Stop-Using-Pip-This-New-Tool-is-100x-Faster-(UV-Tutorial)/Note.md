1. uv is a python package and project manager which is almost 100x faster than pip in certain situations. 

You can install uv using the command: `pip3 install uv`.

Docs:

https://docs.astral.sh/uv/getting-started/installation/
https://docs.astral.sh/uv/

2. We can install various python versions. We can see various python versions that I can install and all python versions which I have downloaded using `uv python list` command.

To install a specific python version, use the `uv python install 3.15` command. It installed very quickly.

To search a particular python version, use the `uv python find 3.8` command.

You can uninstall a particular python version using the `uv python uninstall 3.8` command.

We can run a python script using a particular version as `uv run --python 3.9.21 main.py`. To run a python script by installing a particular library as `uv run --with rich --with requests --python 3.9 main.py` will run main.py with rich and requests library on python 3.9.

3. For a project, pyproject.toml is equivalent to requirements.txt but it is detailed one. uv is going to handle everything for us. 

uv.lock is similar to package-json.lock file as in npm/react/node.js etc.

If we add a new library like pygame in dependencies in pyproject.toml, uv will install it for us automatically when we run `uv run main.py` because in the background, `uv run` command runs `uv sync` command. Or after changing pyproject.toml file, we can run `uv sync` command to install all dependencies.

We can generate the lock file by running `uv lock` command manually. It will resolve everything and create a new uv.lock file for us. Also, we can generate the lock file by running `uv sync` command automatically. 
