#!/bin/bash

# Create layer directory structure
mkdir -p .aws-sam/layers/python/lib/python3.12/site-packages

# Create and activate virtual environment
python3 -m venv ~/.venv/rag-sam
source .venv/rag-sam/bin/activate

# Install dependencies into layer directory
# https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/layer-python/layer-numpy/1-install.sh
pip install \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    --target .aws-sam/layers/python/lib/python3.12/site-packages \
    -r aws/requirements.txt
    

# Deactivate virtual environment
deactivate

# Create ZIP file of the layer (optional)
cd .aws-sam/
zip -r dependencies.zip .
cd ../..