#!/bin/bash

# Install pip if it's not available
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput