set -ex
find /usr -name EXTERNALLY-MANAGED -delete
pip install poetry
poetry config virtualenvs.in-project true
poetry install