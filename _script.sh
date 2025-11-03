# # # Python and venv

# Installing python, pip and venv
sudo apt -y install python3.11
sudo apt -y install python3-pip
sudo apt -y install python3.11-venv

# Creating the venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
which python
which pip

# Installing libraries
vi requirements.txt
fastapi[standard]>=
SQLAlchemy>=
passlib>=
bcrypt>=
python-jose>=
python-dotenv>=
pydantic>=

pip install -r requirements.txt
pip list




# # # Github
https://github.com/adeloaleman and create a repository: fastapi
https://github.com/github/gitignore
vi .gitignore
touch README.md
git init
git branch -M main
git branch --show-current
git add .
git add -A
git commit -m 'first commit'
git remote add origin git@github.com:adeloaleman/fastapi.git
git remote add origin git@github-codeastute:codeastute/fastapi.git
git remote set-url origin git@github.com:adeloaleman/fastapi.git
git push -u origin main




# # # Fastapi project
vi .env
AUTH_SECRET_KEY= 
AUTH_ALGORITHM=
API_URL=http://localhost:3000

touch Procfile

mkdir api
touch api/__init__.py
touch api/main.py
touch api/database.py
touch api/models.py
touch api/deps.py
mkdir api/routers
touch api/routers/__init__.py
touch api/routers/auth.py




mkdir .vscode
vi .vscode/settings.json
{
    "explorer.sortOrder": "filesFirst"
}