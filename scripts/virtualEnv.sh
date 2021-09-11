if [ -d "venv" ]
then
    echo "Virtualenv already exists." 
else
    echo "Virtualenv does not exist."
    virtualenv -p python3 venv
fi

source venv/bin/activate
sleep 1
pip install -r requirements.txt
python main_run.py