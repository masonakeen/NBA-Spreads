#/bash
# a bash script to setup the environment for the project

# install pip3 and virtualenv
sudo apt-get install python3-pip -y

# create the virutual environment in the project root
pip3 install virtualenv
virtualenv -p python3 nba_moneyline

# activate the virtual environment
source nba_moneyline/bin/activate

# install packages you will need
pip3 install -r setup/requirements.txt

python3 -m ipykernel install — user — name nba_moneyline — display-name "Custom NBA ML Kernel"
