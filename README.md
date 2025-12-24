# 🚗 Honda Vehicle History Portal with AI-Powered Service Recommendations
**Flask • MySQL • Machine Learning • Random Forest • Real-time Predictions**

A comprehensive vehicle service management system with an integrated ML-based recommendation engine that predicts maintenance issues based on historical service patterns. The system provides role-based access for employees and customers, complete CRUD operations, and intelligent service suggestions powered by a trained Random Forest classifier.

## 📋 Project Overview

This portal simulates a professional Honda service center management system featuring:

- **Employee Portal** - Complete vehicle management with CRUD operations
- **Customer Portal** - View personal vehicle history and service records  
- **AI Service Predictor** - ML-powered recommendations based on vehicle age and mileage
- **VIN Search System** - Quick vehicle lookup by VIN number
- **Real-time Dashboard** - Live statistics and insights
- **Secure Authentication** - Role-based access control with session management

The ML recommendation system analyzes **1000+ historical service records** to predict likely maintenance issues, categorized by priority (High/Medium/Low) to help service centers proactively identify problems.

---

## 🎯 Key Features

### Security & Authentication
-  **Role-Based Access Control** (Employee/Customer)
-  **Secure Session Management** with password protection
-  **Password Visibility Toggle** on all login forms
-  **Customer Data Isolation** - Users only see their own vehicles

### Vehicle Management
-  **Full CRUD Operations** (Create, Read, Update, Delete)
-  **VIN-based Search** for quick vehicle lookup
-  **Mileage Tracking** for predictive maintenance
-  **Owner Information Management**

### AI/ML Intelligence
-  **Service Issue Prediction** using Random Forest (75-80% accuracy)
-  **Priority-Based Classification** (High/Medium/Low urgency)
-  **Real-time Recommendations** during vehicle intake
-  **1000+ Training Records** with realistic service patterns
-  **20 Service Issue Types** including:
    - Engine Oil Change, Brake Pad Replacement
    - Battery Replacement, Timing Belt Replacement
    - Transmission Fluid Change, AC Gas Refill
    - And 14+ more common issues

### User Experience
-  **Professional UI** with Honda branding
-  **Responsive Design** with Bootstrap 5
-  **Real-time Statistics** dashboards
-  **Color-coded Priority Indicators**
-  **Intuitive Navigation** with breadcrumbs

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                        │
│  ┌──────────────┐  ┌───────────────────┐  ┌──────────────┐  │
│  │    Routes    │  │    ML Predictor   │  │   Session    │  │
│  │   (app.py)   │  │ (ml_predictor.py) │  │  Management  │  │
│  └──────────────┘  └───────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌────────────────────────────┐  ┌────────────────────────────┐
│  MySQL Database            │  │  ML Model Files (.pkl)     │
│  - vehicles table          │  │  - Random Forest Model     │
│  - employees table         │  │  - Label Encoders          │
│  Service history (csv)     │  │  - Feature Info            │
└────────────────────────────┘  └────────────────────────────┘
```

### Data Flow for ML Predictions

```
Employee adds vehicle → Extract features (company, model, year, mileage)
                              ↓
                    ML Model analyzes patterns
                              ↓
                    Predicts likely issues
                              ↓
                    Categorizes by priority
                              ↓
              Displays recommendations to employee
```

---

## 📁 Directory Structure

```
HONDA_INTERNSHIP/
│
├── Project/
│   ├── templates/
│   │   └── index.html                 # Main template (all pages)
│   │
│   ├── app.py                         # Flask routes & logic
│   ├── crud.py                        # Database operations
│   ├── ml_predictor.py                # ML prediction system
│   │
│   ├── generate_dataset.py            # Dataset generator (1000 records)
│   ├── train_model.py                 # Model training script
│   ├── evaluate_model.py              # To test the ML model
│   │
│   ├── vehicle_service_history.csv    # Training dataset
│   ├── service_recommendation_model.pkl
│   ├── mlb_encoder.pkl
│   ├── company_encoder.pkl
│   ├── model_encoder.pkl
│   └── feature_info.pkl
│
├── requirements.txt                   # Python dependencies
└── README.md
```

---

## 🖼️ Project Screenshots

### Landing Page
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b0066ea4-c04c-42e3-bbf3-f3d35c4d5107" />

*Professional landing page with Honda branding and service highlights*

### Employee Dashboard
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d589415d-c00d-4bcc-80ca-746456425e2e" />

*Complete vehicle management interface with VIN search and CRUD operations*

### AI Service Recommendations
<img width="1754" height="982" alt="image" src="https://github.com/user-attachments/assets/b029d006-543c-431f-ada8-3e708aabfa3a" />

*Real-time AI predictions showing prioritized maintenance recommendations*

### Vehicle Search Results
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/91d25d44-eecf-4f40-a53c-0fa7510c7b7e" />

*Quick vehicle lookup by VIN number with detailed information*

### Customer Portal
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/15540e3d-be53-4940-9c92-0b04b19c31f8" />

*Customer-specific view showing only their registered vehicles*

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Chandan-1206/automotive-service-history.git
cd automotive-service-history/Project
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup MySQL Database
```bash
python dbsetup.py
```
*Creates `automotive_db` with 50 sample records in `vehicles` table and 5 in `employees` table*

### 4️⃣ Generate Training Dataset
```bash
python generate_dataset.py
```
*Creates `vehicle_service_history.csv` with 1000 synthetic service records*

### 5️⃣ Train ML Model
```bash
python train_model.py
```
*Trains Random Forest model and saves 5 `.pkl` files (~2 minutes)*

### 6️⃣ Verify Setup (Optional)
```bash
python evaluate_model.py
```
*Runs comprehensive tests to ensure everything works*

### 7️⃣ Run Application
```bash
python app.py
```

### 8️⃣ Access Portal
- **Main Portal:** http://localhost:5000
- **Employee Login:** EMP001 / admin123
- **Customer Login:** Use owner name from database

---

## 🎓 ML Model Details

### Algorithm: Random Forest (Multi-Output Classification)

**Training Configuration:**
- **Estimators:** 100 trees
- **Max Depth:** 15
- **Training Set:** 800 records (80%)
- **Test Set:** 200 records (20%)
- **Accuracy:** 75-80% (1 - Hamming Loss)

**Feature Engineering:**
```python
Features = [
    'company_encoded',      # Honda, Tata, Maruti, Hyundai, Toyota
    'model_encoded',        # 35+ vehicle models
    'year',                 # Manufacturing year
    'vehicle_age',          # Calculated as (2024 - year)
    'mileage'               # Current odometer reading
]
```

**Output Predictions (20 Service Issues):**
- Engine Oil Change
- Brake Pad Replacement
- Battery Replacement
- Timing Belt Replacement
- Clutch Replacement
- Transmission Fluid Change
- AC Gas Refill
- Spark Plug Replacement
- Air Filter Replacement
- Coolant Flush
- Suspension Check
- Shock Absorber Replacement
- And 8 more...

**Prediction Logic:**
```
Age-based Rules:
  Vehicle Age ≥ 5 years → High probability: Timing Belt, Clutch
  Vehicle Age ≥ 3 years → Medium probability: Battery, Suspension

Mileage-based Rules:
  Mileage > 80,000 km → High probability: Transmission, Brakes
  Mileage > 50,000 km → Medium probability: Spark Plugs, Coolant
  Mileage > 30,000 km → Low probability: Air Filter

Common Maintenance:
  80% probability: Engine Oil Change (all vehicles)
  30% probability: Tire Rotation
  25% probability: Wheel Alignment
```

---

## 💡 Usage Examples

### Employee Workflow
1. Login with employee credentials
2. Navigate to "Add Vehicle"
3. Enter vehicle details including **mileage** (critical for ML)
4. Submit form
5. View AI-powered service recommendations categorized by priority
6. Use recommendations for inspection checklist

### Customer Workflow
1. Login with owner name and password (set by employee)
2. View all registered vehicles
3. Check service history

### VIN Search
1. Employee dashboard → VIN Search card
2. Enter VIN number (e.g., VIN1000)
3. View complete vehicle details instantly

---

## 🔧 Configuration

### Update Database Credentials
Edit `crud.py`and `dbsetup.py` before executing:
```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",  # Change this to your mysql root password
        database="automotive_db"
    )
```

### Adjust ML Model
Edit `train_model.py`:
```python
base_classifier = RandomForestClassifier(
    n_estimators=100,      # Increase for better accuracy
    max_depth=15,          # Adjust complexity
    min_samples_split=5,
    random_state=42
)
```

---

## 📊 Database Schema

### `employees` Table
| Column      | Type         | Description           |
|-------------|--------------|-----------------------|
| id          | INT (PK)     | Auto-increment ID     |
| employee_id | VARCHAR(50)  | Unique employee ID    |
| password    | VARCHAR(100) | Authentication        |

### `vehicles` Table
| Column         | Type          | Description              |
|----------------|---------------|--------------------------|
| id             | INT (PK)      | Auto-increment ID        |
| vin            | VARCHAR(50)   | Vehicle Identification # |
| license_plate  | VARCHAR(50)   | Registration plate       |
| model          | VARCHAR(100)  | Vehicle model            |
| year           | INT           | Manufacturing year       |
| owner_name     | VARCHAR(100)  | Customer name            |
| owner_contact  | VARCHAR(20)   | Phone number             |
| password       | VARCHAR(100)  | Customer login           |
| mileage        | INT           | Current mileage (km)     |

---

## 🛡️ Security Features

- **Password Protection:** All accounts require authentication
- **Session Management:** Secure Flask sessions with secret key
- **Role-Based Access:** Employees can't access customer routes and vice versa
- **SQL Injection Prevention:** Parameterized queries throughout
- **Data Isolation:** Customers only see their own vehicles
- **Password Visibility Toggle:** User-friendly authentication

---

## 🎯 Learning Outcomes

### Web Development
✓ Full-stack Flask application development  
✓ Template rendering with Jinja2  
✓ RESTful API design  
✓ Session-based authentication  
✓ Responsive UI with Bootstrap 5  

### Database Management
✓ MySQL database design  
✓ CRUD operations  
✓ Data normalization  
✓ Query optimization  

### Machine Learning
✓ Dataset generation and preprocessing  
✓ Feature engineering  
✓ Multi-output classification  
✓ Random Forest algorithm  
✓ Model evaluation and deployment  
✓ Real-time prediction systems  

### Software Engineering
✓ Modular code architecture  
✓ Error handling and validation  
✓ Version control with Git  
✓ Documentation and README writing  
✓ Production-ready deployment  

---

## 🚨 Troubleshooting

### Issue: ML Model Not Loading
**Solution:** Ensure all 5 `.pkl` files exist in the Project folder. Re-run `train_model.py`.

### Issue: Mileage Showing as 0
**Solution:** Verify `mileage` column exists in database:
```sql
ALTER TABLE vehicles ADD COLUMN mileage INT DEFAULT 0;
```

### Issue: Login Failed
**Solution:** Check credentials in database. Reset employee password:
```sql
UPDATE employees SET password='admin123' WHERE employee_id='EMP001';
```

### Issue: Port Already in Use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

---

## 🔮 Future Enhancements

- [ ] **PDF Report Generation** - Export service history as PDF
- [ ] **Email Notifications** - Alert customers about upcoming services
- [ ] **Service History Timeline** - Visual timeline of past services
- [ ] **Parts Inventory Management** - Track spare parts stock
- [ ] **Appointment Scheduling** - Book service appointments online
- [ ] **Payment Integration** - Process payments securely
- [ ] **Advanced Analytics** - Revenue trends, popular services
- [ ] **Mobile App** - Native Android/iOS application
- [ ] **Multi-location Support** - Manage multiple service centers
- [ ] **Deep Learning Models** - LSTM for time-series predictions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Your Name**  
- GitHub: https://github.com/Chandan-1206/
- LinkedIn: https://www.linkedin.com/in/chandan-agarwal-823b47280/

---

## 🙏 Acknowledgments

- **Flask Documentation** - Web framework guidance
- **scikit-learn** - ML library and algorithms
- **Bootstrap** - UI framework
- **Font Awesome** - Icon library
- **Honda** - Brand inspiration and design

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ for the automotive service industry

</div>
