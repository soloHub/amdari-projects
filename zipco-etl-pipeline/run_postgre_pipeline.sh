#!/bin/bash

# Path to virtual environment
VENV_PATH="/Users/solomonkareem/Data-Engineering-Projects/amdari-projects/.venv"

# Path to your Python file
PYTHON_FILE="/Users/solomonkareem/Data-Engineering-Projects/amdari-projects/zipco-etl-pipeline/postgre_pipeline.py"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python file
python "$PYTHON_FILE"

# Deactivate the virtual environment after execution
deactivate