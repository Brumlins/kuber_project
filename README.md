#POSTUP

python -m venv .venv
. .venv/bin.activate

pip install -r requirements.txt
pip freeze > requirements.txt

docker build -t test .
docker run -p 5000:5000 test

