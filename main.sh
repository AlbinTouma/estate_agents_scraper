
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source $PROJECT_DIR/.env/bin/activate
python dublin.py

git add .
git commit -m 'pushing new data'
git push
