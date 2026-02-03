# Chemical Equipment Parameter Visualizer

A hybrid web + desktop application for visualizing chemical equipment parameters. This project includes a Django REST API backend, a React web frontend, and a PyQt5 desktop application.

![Chemical Equipment Visualizer](https://via.placeholder.com/800x400/1e1b4b/8b5cf6?text=Chemical+Equipment+Visualizer)

## 🏗️ Project Structure

```
├── backend/              # Django REST API
│   ├── config/          # Django project settings
│   └── core/            # Main application
├── web-frontend/        # React + Vite web application
├── desktop-frontend/    # PyQt5 desktop application
├── sample_equipment_data.csv
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### 1. Backend Setup

```bash
# Navigate to project root
cd C:\FOSS

# Activate virtual environment
.\venv\Scripts\activate

# Navigate to backend
cd backend

# Run migrations (already done, but if needed)
python manage.py migrate

# Create superuser (already done, but if needed)
python manage.py create_superuser

# Start the Django server
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

### 2. Web Frontend Setup

```bash
# In a new terminal, navigate to web frontend
cd C:\FOSS\web-frontend

# Install dependencies (already done)
npm install

# Start the development server
npm run dev
```

The web app will be available at: `http://localhost:5173`

### 3. Desktop Application

```bash
# In a new terminal, navigate to project root
cd C:\FOSS

# Activate virtual environment
.\venv\Scripts\activate

# Run the desktop app
python desktop-frontend\main.py
```

## 🔑 Default Credentials

| Username | Password |
|----------|----------|
| admin    | admin123 |

## 📊 Features

### Backend (Django + DRF)
- ✅ RESTful API with Django REST Framework
- ✅ CSV file upload with Pandas processing
- ✅ Automatic batch management (keeps last 5 uploads)
- ✅ Dashboard statistics endpoint
- ✅ PDF report generation with ReportLab
- ✅ Token-based authentication
- ✅ CORS support for frontend apps

### Web Frontend (React)
- ✅ Modern UI with glassmorphism design
- ✅ Drag-and-drop CSV upload
- ✅ Interactive data table
- ✅ Chart.js visualizations (Bar & Scatter)
- ✅ PDF report download
- ✅ Responsive design

### Desktop Frontend (PyQt5)
- ✅ Native Windows application
- ✅ Dark theme matching web UI
- ✅ Matplotlib visualizations
- ✅ Data table view
- ✅ CSV upload dialog
- ✅ PDF report generation

## 📁 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/token/` | Get authentication token |
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/dashboard/` | Get dashboard statistics |
| GET | `/api/equipment/` | List equipment data |
| GET | `/api/report/pdf/` | Download PDF report |

## 📋 CSV Format

The CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,45.2,280.0
```

| Column | Type | Description |
|--------|------|-------------|
| Equipment Name | String | Name of the equipment |
| Type | String | Equipment type (Reactor, Pump, etc.) |
| Flowrate | Float | Flow rate value |
| Pressure | Float | Pressure value |
| Temperature | Float | Temperature value |

## 🧪 Sample Data

A sample CSV file is provided: `sample_equipment_data.csv`

You can use this to test the upload functionality.

## 🛠️ Tech Stack

**Backend:**
- Python 3.x
- Django 6.0
- Django REST Framework
- Pandas
- ReportLab

**Web Frontend:**
- React 18
- Vite
- Chart.js / react-chartjs-2
- Axios
- React Router DOM

**Desktop Frontend:**
- Python 3.x
- PyQt5
- Matplotlib
- Requests

## 📝 License

This project is for educational purposes.

---

Built with ❤️ using Django, React, and PyQt5
