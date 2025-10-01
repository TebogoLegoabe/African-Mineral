# African Critical Minerals Application - Quick Documentation

## 📁 Project Structure

```
african-minerals-app/
├── app.py                          # Main Flask application (entry point)
├── modules/
│   ├── auth.py                    # User authentication & permissions
│   ├── database.py                # Data management (Excel → JSON)
│   ├── visualization.py           # Interactive maps (Folium)
│   └── analytics.py               # Charts & statistics (Plotly)
├── templates/
│   ├── base.html                  # Master template (nav, footer)
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login form
│   ├── dashboard.html             # Main dashboard
│   ├── minerals.html              # Mineral database table
│   ├── countries.html             # Countries list
│   ├── country_profile.html       # Country details
│   ├── map.html                   # Interactive map
│   └── analytics.html             # Charts dashboard
└── data/
    ├── Example...xlsx             # Source data (your Excel file)
    ├── users.json                 # User accounts (auto-generated)
    ├── minerals.json              # Mineral records (auto-generated)
    └── deposits.json              # GPS locations (auto-generated)
```

---

## 🔧 Core Modules

### **app.py** - Main Application

```python
# What it does:
- Defines all URL routes (/, /login, /minerals, /map, etc.)
- Handles HTTP requests (GET/POST)
- Connects modules together
- Renders HTML templates with data

# Key routes:
/ → Landing page
/login → User login
/dashboard → Main dashboard (after login)
/minerals → Database with filters
/map → Interactive map
/countries → Country list
/country/<name> → Country profile
/analytics → Charts & stats
```

### **modules/auth.py** - Authentication

```python
class Authentication:
    # Purpose: Handle user login and permissions

    login(username, password)
        → Validates credentials
        → Returns user data if correct

    register(username, password, email, role)
        → Creates new user account
        → Hashes password (SHA-256)

    check_permission(role, permission)
        → Returns True if role has permission
        → Used for access control
```

### **modules/database.py** - Data Management

```python
class MineralDatabase:
    # Purpose: Load Excel data and provide search functions

    load_excel_data()
        → Reads Excel file
        → Converts to JSON
        → Creates 47 mineral records from 11 minerals

    search_minerals(filters)
        → Filters by mineral name, country
        → Returns matching records

    get_minerals_by_country(country)
        → Returns all minerals for one country

    get_deposits(mineral, country)
        → Returns deposit locations with GPS
```

### **modules/visualization.py** - Maps

```python
class MapVisualization:
    # Purpose: Create interactive maps

    generate_map(deposits)
        → Creates Folium map centered on Africa
        → Adds colored markers for each deposit
        → Includes legend, popups, zoom controls
        → Returns HTML string
```

### **modules/analytics.py** - Charts

```python
class Analytics:
    # Purpose: Generate Plotly charts

    generate_production_by_country(mineral)
        → Bar chart: countries vs production

    generate_market_share_pie(mineral)
        → Pie chart: country market shares

    generate_price_comparison()
        → Bar chart: mineral prices

    generate_top_producers(limit)
        → Bar chart: top producing countries
```

---

## 🔄 How It Works

### **Request Flow**

```
User clicks "Minerals"
  ↓
Browser: GET /minerals
  ↓
app.py: minerals() function
  ↓
database.py: search_minerals()
  ↓
Loads minerals.json
  ↓
Returns data to app.py
  ↓
app.py: render_template('minerals.html', data)
  ↓
Browser: Displays HTML page
```

### **Data Flow**

```
Excel File (source)
  ↓
database.py reads on startup
  ↓
Converts to JSON
  ↓
minerals.json (47 records)
deposits.json (9 locations)
  ↓
Used by all modules
```

### **Authentication Flow**

```
User submits login form
  ↓
app.py: calls auth.login()
  ↓
auth.py: checks password
  ↓
If valid: Create session
  ↓
session['user_id'] = user_id
session['role'] = 'Administrator'
  ↓
User can access protected pages
```

---

## 📄 Templates

### **base.html**

- Master template for all pages
- Includes: navbar, flash messages, footer
- Other templates extend this

### **Page Templates**

```
index.html          → Landing page with features
login.html          → Login form
dashboard.html      → Stats cards + quick links
minerals.html       → Filter form + data table
map.html            → Filter form + embedded map
countries.html      → Country cards grid
country_profile.html → Country details + stats
analytics.html      → Chart selection dashboard
```

---

## 🗄️ Data Storage

### **users.json**

```json
[
  {
    "id": "uuid",
    "username": "admin",
    "password": "hashed_password",
    "email": "admin@example.com",
    "role": "Administrator"
  }
]
```

### **minerals.json**

```json
[
  {
    "id": "uuid",
    "mineral_name": "Cobalt",
    "country": "DRC",
    "production_volume": 130000,
    "reserves": 9750000,
    "price": 32000,
    "uses": "Batteries, catalysts...",
    "year": 2024
  }
]
```

### **deposits.json**

```json
[
  {
    "id": "uuid",
    "mineral": "Cobalt",
    "location_name": "Tenke Fungurume",
    "country": "DRC",
    "latitude": -10.6,
    "longitude": 26.1,
    "reserves": 3600000,
    "annual_production": 130000,
    "status": "Active"
  }
]
```

---

## 🎯 Key Functions

### **Login Required Decorator**

```python
@login_required
def protected_page():
    # This page requires login
    # Decorator checks if user is logged in
    # If not, redirects to /login
```

### **Role-Based Access**

```python
# In app.py
if auth.check_permission(session['role'], 'edit_all'):
    # User can edit data
else:
    # Show error or redirect
```

### **Template Variables**

```python
# In app.py
return render_template('page.html',
    minerals=data,           # Pass data to template
    user=current_user        # Pass user info
)

# In template
{{ minerals|length }}        # Show count
{% for m in minerals %}      # Loop through
```

---

## 🚀 Running the App

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 2. Start server
python app.py

# 3. Open browser
http://localhost:5000

# 4. Login
admin / admin123
```

---

## 📊 Features Summary

| Feature          | Module           | Template              | Route                             |
| ---------------- | ---------------- | --------------------- | --------------------------------- |
| Login            | auth.py          | login.html            | /login                            |
| Dashboard        | app.py           | dashboard.html        | /dashboard                        |
| Mineral List     | database.py      | minerals.html         | /minerals                         |
| Country Profile  | database.py      | country_profile.html  | /country/<name>                   |
| Interactive Map  | visualization.py | map.html              | /map                              |
| Production Chart | analytics.py     | production_chart.html | /analytics/production/<mineral>   |
| Market Share     | analytics.py     | market_share.html     | /analytics/market-share/<mineral> |

---

## 🔐 User Roles & Permissions

| Role          | View Data | Edit Data | Analytics | Manage Users |
| ------------- | --------- | --------- | --------- | ------------ |
| Administrator | ✅        | ✅        | ✅        | ✅           |
| Investor      | ✅        | ❌        | ✅        | ❌           |
| Researcher    | ✅        | ❌        | ✅        | ❌           |

---

## 📝 Adding New Features

### **Add New Route**

1. Add function to `app.py`
2. Create template in `templates/`
3. Add link in `base.html` navigation

### **Add New Database Function**

1. Add method to `database.py`
2. Use in route handler in `app.py`

### **Add New Chart**

1. Add method to `analytics.py`
2. Create route in `app.py`
3. Create template to display chart

---

## 🐛 Common Issues

| Problem               | Solution                               |
| --------------------- | -------------------------------------- |
| Template not found    | Check file is in `templates/` folder   |
| Data not loading      | Ensure Excel file is in `data/` folder |
| Login fails           | Check `data/users.json` exists         |
| Map not showing       | Check internet (needs OpenStreetMap)   |
| Charts not displaying | Install plotly: `pip install plotly`   |

---

## 📚 Technologies

- **Flask**: Web framework (routes, templates)
- **Pandas**: Excel/CSV processing
- **Folium**: Interactive maps
- **Plotly**: Interactive charts
- **Bootstrap**: CSS styling
- **JSON**: Data storage

---

## 🎓 Understanding the Code

**Start Here:**

1. Read `app.py` - see all routes
2. Look at `modules/database.py` - see how data loads
3. Check `templates/base.html` - see page structure
4. Explore templates - see how data displays

**Key Concepts:**

- **Routes**: URLs that trigger Python functions
- **Templates**: HTML files with variables ({{ }})
- **Session**: Stores user login info
- **Decorators**: @login_required, @app.route()
- **JSON**: Text files storing structured data

---

## 📞 Quick Reference

```python
# Get all minerals
minerals = db.get_all_minerals()

# Search with filter
results = db.search_minerals({'country': 'DRC'})

# Generate map
map_html = viz.generate_map(deposits)

# Create chart
chart_html = analytics.generate_production_by_country('Cobalt')

# Check permission
if auth.check_permission('Administrator', 'edit_all'):
    # Allow editing

# Flash message
flash('Success!', 'success')

# Render template
return render_template('page.html', data=data)
```

---

**🎉 That's it! You now understand the entire application structure.**
