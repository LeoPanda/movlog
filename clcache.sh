 find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | grep -v ".venv" | xargs rm -rf

