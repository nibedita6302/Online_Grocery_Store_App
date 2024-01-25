#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "../.myenv" ];
then
    echo "../.myenv folder exists. Installing using pip"
else
    echo "creating .myenv and install using pip"
    python3 -m venv .myenv
fi

# Activate virtual env
. ../.myenv/bin/activate

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt
# Work done. so deactivate the virtual env
deactivate
