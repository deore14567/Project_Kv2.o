# आशापुरी कॉम्प्युटर सर्विस कर्ले 💻 — Village Setu (Local Offline Version)

A **100% offline** version of the Village Setu / Cybercafe Database Management System. No internet required, no cloud database — everything runs locally on your machine using a SQLite file database.

> 🎯 **Designed for:** WSL Ubuntu Linux (Windows Subsystem for Linux). Works on any Debian/Ubuntu-based system.

---

## ✨ Features

- **100% Offline** — No internet, no cloud DB, no Vercel needed
- **SQLite Database** — Local file (`village_setu.db`), zero config
- **One-shot Setup** — `./setup.sh` does everything
- **Farmer Management** — Full CRUD with Aadhaar encryption
- **Farmer Card Generator** — PDF/JPG with QR code, 3 logos
- **Document Vault** — Upload, preview, download
- **Reports** — Export to Excel/PDF/Word/CSV/TXT
- **Multi-language** — English + मराठी (Marathi)
- **Roles** — Admin, Operator, Hidden Super Admin
- **Dark Mode** — Full dark/light theme support

---

## 🚀 Quick Start (One Command)

```bash
git clone https://github.com/deore14567/Project_Kv2.o.git
cd Project_Kv2.o
chmod +x setup.sh
./setup.sh
```

That's it! The script will:
1. ✅ Check Python 3.10+ is installed
2. ✅ Create a virtual environment (`.venv/`)
3. ✅ Install all Python dependencies
4. ✅ Generate a `.env` file with random secrets
5. ✅ Initialize the SQLite database (creates tables + seeds admin)
6. ✅ Start the server at **http://localhost:8000**

Then open http://localhost:8000 in your browser and log in:
- **Email:** `admin@villagesetu.gov.in`
- **Password:** `Admin@12345`

---

## 📋 Prerequisites

### WSL Ubuntu Linux

Install Python and pip if not already present:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

That's all you need. No PostgreSQL, no Docker, no cloud account.

---

## 🔄 Daily Usage (After First Setup)

After running `setup.sh` once, use `run.sh` for daily startup:

```bash
./run.sh
```

This skips the installation steps and just starts the server.

---

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## 📁 Where is My Data?

All data is stored locally in these files/folders:

| File/Folder | What's in it |
|---|---|
| `village_setu.db` | SQLite database (all farmers, users, documents, audit logs) |
| `uploads/` | Uploaded document files (if stored on disk) |
| `.env` | Configuration (secrets, admin credentials) |

To **backup** your data: copy `village_setu.db` and `uploads/` to a safe location.

To **reset** everything: delete `village_setu.db` and run `./setup.sh` again.

---

## 👤 User Roles

### Admin
- Full access to everything
- Can manage users, farmers, documents, reports
- Can reveal/unmask Aadhaar numbers

### Operator
- Can manage farmers and documents
- Cannot delete users or view audit logs
- Can reveal/unmask Aadhaar numbers

### Super Admin (Hidden)
- **Login:** `rohit.deore@ashapuricomputer.in` (password set via `/setup-superadmin.html`)
- **Setup key:** `8329977647`
- Hidden from user list
- Actions NOT logged in audit trail
- Full admin privileges

---

## 🌐 Accessing from Another Computer on LAN

The server binds to `0.0.0.0:8000`, so other computers on your local network can access it:

1. Find your IP: `ip addr show eth0 | grep inet`
2. On another computer, open: `http://YOUR-IP:8000`

---

## 📁 Folder Structure

```
Project_Kv2.o/
├── setup.sh                 # One-shot setup script (run this first)
├── run.sh                   # Daily start script
├── .env                     # Auto-generated config (created by setup.sh)
├── .env.example             # Template for .env
├── requirements.txt         # Python dependencies
├── village_setu.db          # SQLite database (auto-created)
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings (SQLite by default)
│   ├── database.py          # Engine + session management
│   ├── models.py            # Database models
│   ├── auth.py              # JWT + bcrypt authentication
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── schemas/             # Pydantic schemas
│   └── utils/               # Validation, crypto, audit
├── frontend/
│   ├── *.html               # Web pages
│   ├── css/                 # Tailwind CSS (pre-built)
│   ├── js/                  # JavaScript (API client, i18n, card template)
│   └── assets/              # Logos and images
├── uploads/                 # Uploaded files
└── README.md                # This file
```

---

## 🔧 Customization

### Change Admin Credentials
Edit `.env`:
```
ADMIN_EMAIL=your@email.com
ADMIN_PASSWORD=YourPassword123
```
Then delete `village_setu.db` and run `./setup.sh` again.

### Change Port
Edit `run.sh` or `setup.sh`:
```bash
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 9000
```

### Use PostgreSQL Instead of SQLite
Edit `.env`:
```
DATABASE_URL=postgresql+psycopg2://user:pass@host:port/dbname
```
Install psycopg2: `pip install psycopg2-binary`

---

## 🆘 Troubleshooting

### "python3: command not found"
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### "Port 8000 already in use"
```bash
# Find what's using port 8000
sudo lsof -i :8000
# Kill it, or use a different port in run.sh
```

### Database locked / corrupted
```bash
# Stop the server, then:
rm village_setu.db
./run.sh  # Re-initializes the database
```

### Forgot admin password
```bash
# Stop the server, then:
rm village_setu.db
./setup.sh  # Recreates with default password Admin@12345
```

---

## 📜 License

This project is provided as-is for the आशापुरी कॉम्प्युटर सर्विस कर्ले use case.

---

## 🆕 Differences from Cloud Version (Project_K)

| Feature | Project_K (Cloud) | Project_Kv2.o (Local) |
|---|---|---|
| Database | PostgreSQL (Aiven/Neon) | SQLite (local file) |
| Internet required | Yes | **No** |
| Setup | Vercel + env vars | One `./setup.sh` script |
| Database driver | psycopg2 | Built-in sqlite3 |
| Deployment | GitHub → Vercel | Local machine only |
| Data location | Cloud | `village_setu.db` file |

---

Built with ❤️ for offline digital governance.
