# Sri Gajana Generic Medical Store — Website

A full-stack website for a generic medical store with customer and medicine tracking.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python Flask + SQLAlchemy |
| Database | SQLite |

## Project Structure

```
Website_for_MedicalStore/
├── plan.md              # Detailed project plan
├── README.md            # This file
├── backend/             # Flask API
│   ├── app.py           # Main entry point
│   ├── models.py        # SQLAlchemy models
│   ├── routes/
│   │   ├── customers.py # Customer CRUD API
│   │   └── medicines.py # Medicine CRUD API
│   ├── requirements.txt
│   └── Procfile         # Render deployment
└── frontend/            # React app
    ├── src/
    │   ├── api.js       # API client
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   └── Footer.jsx
    │   └── pages/
    │       ├── Home.jsx
    │       ├── About.jsx
    │       ├── Services.jsx
    │       ├── Contact.jsx
    │       └── Dashboard.jsx
    └── package.json
```

## Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# API runs at http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/customers?search=` | List/search customers |
| POST | `/api/customers` | Create customer |
| GET | `/api/customers/:id` | Get customer |
| PUT | `/api/customers/:id` | Update customer |
| DELETE | `/api/customers/:id` | Delete customer |
| GET | `/api/customers/:id/medicines` | List medicines for customer |
| POST | `/api/customers/:id/medicines` | Add medicine record |
| PUT | `/api/medicines/:id` | Update medicine |
| DELETE | `/api/medicines/:id` | Delete medicine |

## Deployment

- **Frontend**: Deploy to [Vercel](https://vercel.com) — connect GitHub repo, set root to `frontend/`
- **Backend**: Deploy to [Render](https://render.com) — connect GitHub repo, set root to `backend/`, build command: `pip install -r requirements.txt`, start command: `gunicorn app:app`