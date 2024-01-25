#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "../.myenv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run local_setup.sh first"
    exit 1
fi

# Activate virtual env
. ../.myenv/bin/activate
export ENV=stage
gunicorn main:app --worker-class gevent --bind 0.0.0.0:8000 --workers=2
deactivate