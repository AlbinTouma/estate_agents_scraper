
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

pip install -r requirements.txt


python dublin.py

git add .
git commit -m 'pushing new data'
git push
