# PostFile
Web app and backend for filing documents.

Code checks
```bash
black . -l 120 && flake8 --max-line-length 120 && mypy . --ignore-missing-imports
```

# Launch Development
```bash
export FLASK_ENV=development
export FLASK_PORT=5000
export SECRET_KEY=1234
export FILES_PATH=
export DETAILS_PATH=
export STORAGE_PATH=
cd web
flask run --port=$FLASK_PORT
```

# Launch Production
```bash
export FLASK_ENV=production
export FLASK_PORT=5000
export SECRET_KEY=
export FILES_PATH=
export DETAILS_PATH=
export STORAGE_PATH=
cd web
flask run --port=$FLASK_PORT
```

# TODO
- Uploads with same name
- Storage transfers with same name