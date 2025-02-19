### **🔥 README: Setting Up CountdownApp with Docker Locally**  
This **README** will guide you on **how to set up and run** the **CountdownApp** (Angular + Django + Redis) using **Docker**.

---

# **📌 CountdownApp - Dockerized Setup**
A full-stack **countdown timer application** built with:
- 🎯 **Django REST Framework (Backend)**
- ⚡ **Angular (Frontend)**
- 🔄 **Redis (WebSockets & Caching)**
- 🐳 **Docker & Docker Compose (Containerization)**
- 🌐 **Nginx (Reverse Proxy & Static File Serving)**

---

## **🚀 Prerequisites**
Before running the project, ensure you have the following installed:
- **Docker** 🐳 → [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** → Comes with Docker (verify with `docker-compose --version`)

---

## **📦 Project Structure**
```
.
├── client/               # Angular frontend (Dockerized)
├── server/               # Django backend (Dockerized)
│   ├── countdown_app/    # Django app (API & WebSockets)
│   ├── timer/            # Timer logic & models
│   ├── tests/            # Backend API tests
│   ├── manage.py         # Django CLI
│   ├── requirements.txt  # Backend dependencies
├── docker/               # Docker & Nginx configurations
│   ├── nginx.conf        # Nginx reverse proxy setup
├── docker-compose.yml    # Multi-container setup
├── Dockerfile.client     # Angular build process
├── Dockerfile.server     # Django backend setup
└── README.md             # Setup guide (this file)
```

---

## **📌 Step 1: Clone the Repository**
```bash
git clone https://github.com/aisamuel/countdown-app.git
cd countdown-app
```

---

## **📌 Step 2: Set Up Environment Variables**
Create a **`.env` file** inside the root directory and copy the content of sample.dev into it:
```ini
# Static & Media Files Configuration
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media

# Database Configuration
USE_SQLITE=False  # Switches between SQLite and PostgreSQL
POSTGRES_DB=timerdb
POSTGRES_USER=timeruser
POSTGRES_PASSWORD=securepassword
POSTGRES_HOST=db
POSTGRES_PORT=5432


# Django Configuration
DJANGO_SECRET_KEY='django-insecure-0d@h8lmg!vaziw2p8@n2ywy-a#dn)iuefa8*e#r6=yh&2f1x_%'
DEBUG=False
ALLOWED_HOSTS=*
DJANGO_SETTINGS_MODULE=countdown_project.settings
USE_LOCAL=False
REDIS_URL=redis://redis:6379
```
✅ **This ensures Django connects to Redis & PostgreSQL inside Docker.**

---

## **📌 Step 3: Build & Run Containers**
Run the following command to **build and start** all containers:
```bash
docker-compose up --build
```
🚀 This will:
- Build and start **Django** (`backend`).
- Build and start **Angular** (`frontend`).
- Start **Redis** (`redis`).
- Start **Nginx** (`nginx`) as a reverse proxy.

✅ **Once running, visit:**
- 🌍 **Frontend (Angular):** [http://localhost:4200/](http://localhost:4200/)
- ⚙️ **Backend API (Django):** [http://localhost/api/](http://localhost/api/)
- 🔄 **WebSockets (Django Channels):** `ws://localhost/ws/timer/1/`

---

## **📌 Step 4: Run Database Migrations**
In a new terminal, apply database migrations:
```bash
docker-compose exec backend python manage.py migrate
```
✅ This will create necessary database tables.

---

## **📌 Step 5: Create a Superuser (For Admin Panel)**
Run the following command to create an **admin user**:
```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## **📌 Step 6: Running Tests**
### **📝 Run Backend API Tests**
```bash
docker-compose exec backend python manage.py test timer.tests
```
✅ This runs all API & model tests.

---

## **📌 Step 7: Stopping the Application**
To **stop all running containers**, run:
```bash
docker-compose down
```
🔹 **Add `-v` to also remove volumes (database & cache):**
```bash
docker-compose down -v
```

---

## **📌 Step 8: Restarting the Application**
If you made **changes and want to restart everything**, run:
```bash
docker-compose down -v  # Stop & remove all containers + volumes
docker-compose up --build  # Rebuild and start fresh
```
✅ This ensures your changes are reflected properly.

---

## **📌 Common Debugging Issues**
### **1️⃣ "ModuleNotFoundError" in Django Backend**
Run:
```bash
docker-compose exec backend pip install -r requirements.txt
```
Then restart:
```bash
docker-compose restart backend
```

### **2️⃣ WebSocket Not Connecting**
- Check Redis is running:
```bash
docker-compose logs redis
```
- If Redis is down, restart it:
```bash
docker-compose restart redis
```

### **3️⃣ Changes Not Reflecting in Angular**
If frontend updates aren't showing:
```bash
docker-compose up --build frontend
```
or force-rebuild:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

---

## **🚀 Final Outcome**
✅ **Frontend (Angular) accessible at `http://localhost:4200/`**  
✅ **Backend API (Django) running at `http://localhost/api/`**  
✅ **WebSockets (Live updates) working at `ws://localhost/ws/timer/`**  
✅ **Fully containerized with Docker & Docker Compose**  

---

## **📌 Assess the App on remotely**
Access the deployed version of the app at:
- 🌐 **[https://distinct-jackal-samuel65-4969e964.koyeb.app/](https://distinct-jackal-samuel65-4969e964.koyeb.app/)**

---

## **📌 Contributors**
👨‍💻 **Your Name** - Developer  
🌐 **GitHub:** [aisamuel](https://github.com/aisamuel)  

---

## **🚀 Now You're Ready to Run CountdownApp!**
🔥 Let me know if you need **more improvements or extra features!** 🚀😊