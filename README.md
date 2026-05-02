# 🌾 SALS — Smart Agricultural Loan System

A Django-based agricultural loan management system built for the **Agricultural Bank of Bangladesh**, designed to help small and marginal farmers access credit easily with automated eligibility scoring, NID verification, and repayment tracking.

---

## ✨ Features

- **Role-based access** — Farmer, Bank Officer, Admin with separate dashboards
- **Loan lifecycle management** — Apply → Score → Approve/Reject → Repay
- **Automated priority scoring** — Scores farmers 0–100 based on income, land size, and loan-to-income ratio, favoring small and low-income farmers
- **NID verification** — Upload NID card (image or PDF), verified by bank officers
- **EMI calculation** — Compound interest formula with monthly installments
- **Repayment tracking** — Record payments, approve/reject, auto-calculate remaining balance
- **PDF generation** — Loan approval letters and repayment receipts
- **Bilingual support** — English and Bengali (বাংলা) with Django i18n
- **Cloud file storage** — Cloudinary for all uploaded documents and images
- **Admin panel** — Custom Django admin with filters, search, and inline views

---

## 👥 User Roles

| Role | Permissions |
|---|---|
| **Farmer** | Register, create profile, upload NID, apply for loan, make repayments |
| **Bank Officer** | Verify NIDs, approve/reject loans, record repayments, view all farmers |
| **Admin** | All officer permissions + full statistics dashboard |

---

## 🔢 Priority Score System

Loans are auto-decided based on a priority score (0–100) that favors deserving farmers:

| Factor | Max Points | Higher score when... |
|---|---|---|
| Income level | 35 | Lower annual income |
| Land size | 30 | Smaller land holding |
| Loan-to-income ratio | 25 | Lower loan amount relative to income |
| Repayment history | 10 | All previous loans fully repaid |

| Score | Decision |
|---|---|
| ≥ 70 | Auto-approved |
| 40–69 | Pending — bank officer review |
| < 40 | Auto-rejected |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Python 3.8+ |
| Database | PostgreSQL (via `dj_database_url`) |
| File storage | Cloudinary |
| Static files | Whitenoise |
| PDF generation | fpdf2 |
| Hosting | Render.com |
| Frontend | Bootstrap 5, Chart.js |

---

## ⚙️ Installation

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd SALS

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
sudo apt install gettext        # Required for translations (Linux)
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Run migrations and create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Compile translations

```bash
python manage.py compilemessages
```

### 6. Run development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — English, `http://127.0.0.1:8000/bn/` — Bengali

---

## 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | Debug mode (`True`/`False`) | ✅ |
| `DATABASE_URL` | PostgreSQL connection URL | ✅ |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | ✅ |
| `CLOUDINARY_API_KEY` | Cloudinary API key | ✅ |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | ✅ |
| `RENDER_EXTERNAL_HOSTNAME` | Render deployment hostname | Production only |
| `EMAIL_HOST` | SMTP host | For password reset |
| `EMAIL_HOST_USER` | Email address | For password reset |
| `EMAIL_HOST_PASSWORD` | Email password | For password reset |

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 Production Deployment (Render)

### build.sh
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
apt-get install -y gettext
python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py migrate
```

### Run command
```bash
gunicorn sals_project.wsgi:application --bind 0.0.0.0:8000
```

---

## 📁 Project Structure

```
SALS/
├── sals_project/           # Django project config
│   ├── settings.py         # Settings (env-based)
│   └── urls.py             # Root URL config
├── loan_app/               # Main application
│   ├── models.py           # User, FarmerProfile, LoanApplication, Repayment
│   ├── views.py            # All view functions + PDF generation
│   ├── forms.py            # Django forms with validation
│   ├── admin.py            # Custom admin configuration
│   ├── urls.py             # App URL routing
│   └── templatetags/       # Custom template filters
├── templates/              # HTML templates (Bootstrap 5)
│   ├── dashboard/          # Role-specific dashboards
│   ├── farmer/             # Farmer profile, NID upload
│   ├── loan/               # Loan apply, history, detail
│   ├── repayment/          # Repayment forms and history
│   ├── bank_officer/       # Officer views
│   └── registration/       # Auth templates
├── locale/                 # Translation files
│   └── bn/                 # Bengali translations
├── static/                 # Static files (CSS, JS)
├── media/                  # Local file uploads (dev only)
├── .env.example            # Environment template
├── build.sh                # Render build script
├── requirements.txt        # Python dependencies
├── COMMANDS.md             # Developer command reference
└── README.md               # This file
```

---

## 💰 Default Loan Types

| Loan Type | Interest Rate | Max Amount |
|---|---|---|
| Crop Loan | 6.0% p.a. | ৳25,00,000 |
| Agricultural Equipment Loan | 8.5% p.a. | ৳50,00,000 |
| Farm Development Loan | 7.5% p.a. | ৳1,00,00,000 |

---

## 🌐 Language Support

The system supports English and Bengali. To switch languages, use the language toggle in the navbar or visit:
- `/en/` — English
- `/bn/` — Bengali

To add new translation strings:
```bash
python manage.py makemessages -l bn --ignore=.venv --ignore=venv
# Edit locale/bn/LC_MESSAGES/django.po
python manage.py compilemessages
```

---

## 📄 License

MIT License