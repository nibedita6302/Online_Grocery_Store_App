#! bin/sh

echo '==================================='
echo 'Setup Local environment'
echo 'Install required Pyhton Libraries'
echo '==================================='

if [ -d '.project-mad1-env' ]; then
	echo '.env folder exists.'
else
	echo 'creating .env folder'
	python3 -m venv ..project-mad1-env 
fi

# Activate virtual env
. .project-mad1-env/bin/activate

#upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt
# Work done -> deactivate virtual env
#deactivate -- not working

