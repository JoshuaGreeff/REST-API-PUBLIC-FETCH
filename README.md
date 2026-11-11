# REST API Public Fetch

A small Flask application that retrieves public NHTSA vehicle-variable data and displays only variables in the **Active Safety System** group.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open `http://127.0.0.1:5000/` in a browser. The page shows a loading message while it fetches data and displays an error message if the request cannot be completed.

## Test

```powershell
python -m unittest discover -s tests -v
```

A successful run reports two passing tests: one verifies the required `GroupName` filter, and one verifies the external-API timeout response.

## Useful route

- `GET /items` returns the filtered JSON list.
