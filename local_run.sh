#! /bin/sh

echo '==================================='
echo 'Setup Local environment'
echo 'Install required Pyhton Libraries'
echo '==================================='

if [ -d '.project-mad1-env' ]; then
	echo 'Enabling virtual environments'
else
	echo 'No virtual environment. Please run local_setup.sh first!'
	exit N
fi

# Activate virtual env
. .project-mad1-env/bin/activate

export ENV=development 
python main.py
deactivate 
