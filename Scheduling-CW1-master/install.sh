# install prerequisites
sudo apt-get -y install python3-venv python3-pip
python3 -m pip install --upgrade pip

# update path
export PATH=$PATH:~/.local/bin

python3 -m pip install -r requirements.txt
sudo chmod 400 keys/id_rsa
sudo chmod +x ./funcstart.sh

# setup azure function tools
wget -q https://packages.microsoft.com/config/ubuntu/19.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get -y update
sudo apt-get -y install azure-functions-core-tools
rm packages-microsoft-prod.deb