cd ../
if [ -d "venv" ]
then
    echo "Virtualenv already exists." 
else
    echo "Virtualenv does not exist. creating."
    virtualenv -p python3 venv
fi

source ./venv/bin/activate
sleep 1
echo "installing requirements"
pip install -r scripts/requirements.txt