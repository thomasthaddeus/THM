@echo off

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo The virtual environment has been set up and packages have been installed.
echo You are currently in the virtual environment. To exit, run the 'deactivate' command.
