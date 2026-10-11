# Sri Gajana Generic Medical Store — Website Plan

## 1. Project Overview

| Field | Detail |
|---|---|
| **Store Name** | Sri Gajana Generic Medical Store |
| **Purpose** | Online presence for a generic medical store with customer & medicine tracking |
| **Target Users** | Store owner, staff, and walk-in customers |
| **Budget** | ₹0 (entirely free tier) |

---

## 2. Tech Stack (All Free Tier)

| Layer | Technology | Free Tier Limit | Why |
|---|---|---|---|
| **Frontend** | React + Vite | Unlimited | Fast, modern SPA; easy to deploy |
| **Styling** | Tailwind CSS | Unlimited | Utility-first, rapid UI development |
| **Backend** | Python Flask | Unlimited | Simple REST API, easy to learn |
| **Database** | SQLite (file-based) | Unlimited | Zero cost, zero server, perfect for small stores |
| **ORM** | SQLAlchemy | Unlimited | Pythonic DB interaction |
| **Hosting (Frontend)** | Vercel | 100 GB bandwidth/month | Free, auto-deploys from GitHub |
| **Hosting (Backend)** | Render | 750 hrs/month (always enough) | Free Flask hosting with HTTPS |
| **Version Control** | GitHub | Unlimited public/private repos | Code storage + CI/CD trigger |
| **Domain (Optional)** | Vercel/Render subdomain | Free `*.vercel.app` / `*.onrender.com` | No custom domain cost |

---

## 3. Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                    USER'S BROWSER                     │
└──────────────────────┬───────────────────────────────┘
                       │ HTTPS
                       ▼
┌──────────────────────────────────────────────────────┐
│              VERCEL (Frontend Hosting)                │
│          React + Tailwind CSS (Static SPA)            │
└──────────────────────┬───────────────────────────────┘
                       │ API Calls (fetch/axios)
                       ▼
┌──────────────────────────────────────────────────────┐
│              RENDER (Backend Hosting)                 │
│          Python Flask REST API                        │
│          SQLAlchemy ORM                               │
│          SQLite Database (file on Render disk)        │
└──────────────────────────────────────────────────────┘
```

> **Note:** SQLite lives on Render's persistent disk. For a small store, this is sufficient. If you need a cloud DB, switch to **Supabase (free PostgreSQL)**.

---

## 4. Features / Pages

### 4.1 Public Pages
| Page | Description |
|---|---|
| **Home** | Store name, tagline, hero section, services overview |
| **About Us** | Store history, mission, team, location |
| **Contact** | Address, phone, email, Google Maps embed |
| **Services** | List of services (generic medicines, home delivery, etc.) |

### 4.2 Admin Dashboard (Password Protected)
| Feature | Description |
|---|---|
| **Customer Management** | Add / View / Edit / Delete customers |
| **Medicine Tracker** | Record which customer took which medicine & when |
| **Search** | Search customers by name or phone number |

### 4.3 Customer Record Fields
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment |
| `name` | String | Customer full name |
| `phone` | String | Contact number |
| `email` | String (optional) | Email address |
| `address` | Text (optional) | Residential address |
| `created_at` | DateTime | Record creation timestamp |

### 4.4 Medicine Record Fields
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment |
| `customer_id` | Integer (FK) | Linked customer |
| `medicine_name` | String | Name of medicine |
| `dosage` | String | e.g., "500mg", "10ml" |
| `quantity` | Integer | Number of units |
| `date_purchased` | Date | When the medicine was taken |
| `notes` | Text (optional) | Any additional notes |
| `created_at` | DateTime | Record creation timestamp |

---

## 5. Database Schema (SQLite)

```sql
CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medicine_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    medicine_name TEXT NOT NULL,
    dosage TEXT,
    quantity INTEGER DEFAULT 1,
    date_purchased DATE DEFAULT (date('now')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);
```

---

## 6. Project Folder Structure

```
Website_for_MedicalStore/
├── plan.md                          # This file
├── frontend/                        # React + Vite app
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── About.jsx
│   │   │   ├── Contact.jsx
│   │   │   ├── Services.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Customers.jsx
│   │   │   └── Medicines.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                         # Python Flask app
│   ├── app.py                       # Main Flask entry point
│   ├── models.py                    # SQLAlchemy models
│   ├── routes/
│   │   ├── customers.py
│   │   └── medicines.py
│   ├── requirements.txt
│   └── Procfile                     # For Render deployment
└── README.md
```

---

## 7. Required Accounts & Tools

### 7.1 Free Accounts to Create

| Platform | Sign-Up Link | Purpose |
|---|---|---|
| **GitHub** | https://github.com | Code repository |
| **Vercel** | https://vercel.com | Host frontend (sign in with GitHub) |
| **Render** | https://render.com | Host backend Flask API (sign in with GitHub) |

### 7.2 Tools to Install Locally

| Tool | Download Link | Purpose |
|---|---|---|
| **Node.js (LTS)** | https://nodejs.org | Run React/Vite dev server |
| **Python 3.10+** | https://python.org | Run Flask backend |
| **VS Code** | https://code.visualstudio.com | Code editor (already installed) |
| **Git** | https://git-scm.com | Version control |

### 7.3 API Keys / Secrets Needed

| Key | Source | Purpose | Cost |
|---|---|---|---|
| **None required** | — | This app has no third-party API dependencies | ₹0 |

> The app is self-contained. No payment gateways, SMS APIs, or external services are needed for the MVP.

---

## 8. Development Phases

### Phase 1: Setup & Backend (Day 1)
- [ ] Create GitHub repository
- [ ] Set up Flask project with SQLAlchemy + SQLite
- [ ] Create Customer & Medicine models
- [ ] Build REST API endpoints (CRUD for customers & medicines)
- [ ] Test API with Postman or curl
- [ ] Deploy backend to Render

### Phase 2: Frontend (Day 2)
- [ ] Scaffold React + Vite + Tailwind project
- [ ] Build public pages: Home, About, Contact, Services
- [ ] Build admin dashboard: Customer list, Add/Edit customer
- [ ] Build medicine tracker: Link medicines to customers
- [ ] Connect frontend to backend API
- [ ] Deploy frontend to Vercel

### Phase 3: Polish (Day 3)
- [ ] Add admin password protection (simple Flask session auth)
- [ ] Add search functionality
- [ ] Mobile responsive testing
- [ ] Final testing & bug fixes

---

## 9. Estimated Costs

| Item | Cost |
|---|---|
| Domain | ₹0 (use Vercel/Render subdomain) |
| Hosting | ₹0 (Vercel + Render free tiers) |
| Database | ₹0 (SQLite on Render) |
| SSL Certificate | ₹0 (auto-provided by Vercel & Render) |
| **Total** | **₹0** |

---

## 10. Optional Upgrades (When Needed)

| Upgrade | Cost Estimate | When to Consider |
|---|---|---|
| Custom domain (e.g., `srigajana.com`) | ~₹800/year | When you want a professional domain |
| Supabase (PostgreSQL) | ₹0 (free tier: 500 MB) | If SQLite file grows too large |
| Cloudflare CDN | ₹0 (free tier) | For faster global loading |
| WhatsApp Business API | ~₹500/month | For automated order notifications |

---

## Next Steps

1. Confirm this plan looks good
2. I'll start building the backend (Flask + SQLite)
3. Then the frontend (React + Tailwind)
4. Finally deploy both to Render & Vercel

Shall I proceed with Phase 1?