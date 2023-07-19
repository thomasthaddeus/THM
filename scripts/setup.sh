#!/bin/bash

# create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install packages
pip install pandas numpy matplotlib seaborn scipy statsmodels nltk sklearn textblob pyLDAvis json base64 worldcloud scikit-learn

# freeze requirements and save to requirements.txt
pip freeze > requirements.txt

# deactivate virtual environment
deactivate
