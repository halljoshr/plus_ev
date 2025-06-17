# Data Dawgs Web Monorepo

This repository contains the full-stack Data Dawgs web application, including a Django backend, a React frontend, and data analysis notebooks.

Originally written in 2024 but moved to github as an example project in 2025.
No longer guarenteed to be working, must have API keys and those have been removed from the code. 

## Project Structure

- `data_dawgs_web/` — Django backend (ASGI, WSGI, API, business logic)
- `frontend/` — React frontend (UI, static assets)
- `pev_app/` — Django app for plus EV betting
- `analysis/` — Jupyter notebooks and scripts for data analysis

## Quick Start

### Backend (Django)

1. Install Python dependencies (recommend using a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Start the backend server (ASGI):
   ```bash
   uvicorn data_dawgs_web.asgi:application --reload
   ```

See `data_dawgs_web/Readme.md` for more backend details.

### Frontend (React)

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm start
   ```

See `frontend/README.md` for more frontend details and available scripts.

### Data Analysis

- Jupyter notebooks and CSV data are in `analysis/notebooks/`.
- Scripts are in `analysis/scripts/`.

## Development Notes

- Python, Django, and Node/React build, cache, and environment files are ignored via `.gitignore`.
- For environment variables, use `.env` files as appropriate (see subproject READMEs).

## License

[MIT](LICENSE) (or specify your license here) 