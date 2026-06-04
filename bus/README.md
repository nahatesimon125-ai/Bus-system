# NTS Regional Bus Tickets Uganda (Django Web Application)

A premium, modern regional bus ticketing and seat booking platform with cashless mobile money simulator support in Uganda, built entirely using **Python 3** & **Django**.

This project does **NOT** use React or Vite. It is a pure Django web application using server-side template rendering (`Django Templates`) and styled dynamically with CDN-loaded `Tailwind CSS` & `Lucide Icons`.

---

## 🚀 How to Run the Server in Your Local Terminal

Follow these exact steps to start the application on your computer:

### 1. Prerequisite: Python 3
Ensure that Python 3 is installed. You can check this by running:
```bash
python --version
# or
python3 --version
```

### 2. Enter the Project Directory
Open your terminal (PowerShell, Command Prompt, or bash) and change to this project directory:
```bash
cd c:/Users/Admin/Desktop/BUS
```

### 3. Install Django
Install Django within your system Python framework or within an active virtual environment:
```bash
pip install django
# or if using python3 on macOS/Linux
python3 -m pip install django
```

### 4. Create and Prepare the Database (Apply Migrations)
This runs the Django migrations to set up the SQLite database structure (creating the standard user, routes, and trips):
```bash
python manage.py makemigrations tickets
python manage.py migrate
```

### 5. Start the Development Server
Run the standard Django development server:
```bash
python manage.py runserver
# or if using python3
python3 manage.py runserver
```

### 6. Access the System
Once started, the server will output typical logs indicating it is active. Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🚌 Features & Default Accounts

Once the server runs, you will be shown the interactive NTS Uganda booking dashboard, matching the design in the preview exactly. The system will pre-seed realistic regional trip schedules (Kampala, Jinja, Mbale, etc.) automatically.

### Demo Login Accounts:
* **Passenger/Customer Account:**
  * **Email:** `customer@nts.ug`
  * **Password:** `password`
* **Transport Fleet Staff Account:**
  * **Email:** `admin@nts.ug`
  * **Password:** `admin`

---

## 📁 Pure Django Project Structure
All modern layout components are stored cleanly in the following server-side directories:
* `/tickets/templates/` — HTML views loaded via standard Django inheritance:
  * `base.html` — Base layout with interactive Tailwind config, font packages, and Lucide CDNs.
  * `trips.html` — Interactive seat-selection grid with simulated cash-free MTN MoMo/Airtel Money checkout channels.
  * `history.html` — Customer Booking history, interactive digital ticket vouchers, and PDF download buttons.
  * `staff.html` — Staff operations dashboard for supervising bus capacities, booking logs, and scheduling departures.
* `/tickets/views.py` — Database views, transaction creation logic, and analytical reports.
* `/tickets/models.py` — SQLite schema definitions: `CustomerUser`, `Bus`, `Route`, `Trip`, `Booking`.
