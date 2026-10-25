# DineFlow: Intelligent Restaurant Management System & DBMS Demonstration

**Developed by:** Gautam Soni  
**Enrollment Number:** `0808CS241120`  
**Department:** Computer Science & Engineering  
**Institution:** Institute of Engineering & Science, IPS Academy, Indore (Session 2026-27)  
**Subject:** Database Management System (DBMS)

---

## 🌟 Project Overview
**DineFlow** is an enterprise-grade Restaurant Management System built with **Python (Flask)** and **SQLite / MariaDB**, purpose-built to demonstrate core and advanced **Database Management System (DBMS)** principles through real-world hospitality workflows.

The system handles both **front-of-house** operations (table reservations, floor layout, customer loyalty, Point-of-Sale billing) and **back-of-house** management (Kitchen Order Tickets, inventory stock levels, Bill of Materials recipe mapping), while enforcing strict data consistency, active automation, and auditability at the database engine level.

---

## 🎯 Key DBMS Concepts Demonstrated

| DBMS Concept | Implementation in DineFlow |
| :--- | :--- |
| **Relational Modeling (12 Tables)** | Normalized schema for Users, Dining Tables, Categories, Menu Items, Customers, Reservations, Orders, Order Items, Payments, Inventory, Recipes (BOM), and Audit Logs. |
| **Normalization (1NF to BCNF)** | Elimination of repeating groups, partial dependencies, and transitive dependencies across all entities. |
| **Integrity Constraints** | Primary Keys (`AUTOINCREMENT`), Foreign Keys (`ON DELETE CASCADE` / `SET NULL`), `CHECK` constraints, `UNIQUE` constraints, and `NOT NULL` rules. |
| **Active Triggers (5 Triggers)** | Autonomous recalculation of order subtotal & 5% GST on item addition/deletion, auto-marking tables as `Occupied` upon ordering, auto-releasing tables upon payment, and audit logging price alterations. |
| **Database Views (5 Views)** | Precomputed virtual tables for Daily Sales, Top Selling Dishes, Live Table Occupancy, Low Stock Warnings, and Staff Performance. |
| **ACID Transactions** | Multi-table atomic checkout coordinating payment creation, order completion, table release, loyalty point crediting, and recipe-based inventory depletion with `COMMIT` and `ROLLBACK` handling. |
| **Query Optimization & Indexes** | B-Tree indexes on foreign keys and search columns, verified via `EXPLAIN QUERY PLAN`. |
| **Interactive DBMS Live Lab** | An in-app console to view schema metadata, run custom SQL queries, test ACID transaction rollback scenarios live, and examine trigger audit trails. |

---

## 📁 Repository Structure
```
DBMS/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # Responsive modern UI styling
│   │   └── js/
│   │       └── main.js              # POS cart, ACID simulator, SQL console AJAX
│   ├── templates/
│   │   ├── base.html                # Base layout with navigation and student badge
│   │   ├── index.html               # Operations Dashboard & live floor plan
│   │   ├── tables.html              # Seating map & reservation system
│   │   ├── menu.html                # Menu catalog & price update triggers
│   │   ├── pos.html                 # Point of Sale & real-time billing
│   │   ├── kitchen.html             # Kitchen Order Ticket (KOT) display system
│   │   ├── inventory.html           # Raw stock & Recipe Bill of Materials (BOM)
│   │   ├── dbms_concepts.html       # Interactive DBMS Demonstration Lab
│   │   └── reports.html             # Analytical reports powered by SQL views
│   ├── __init__.py                  # Flask app factory and API endpoints
│   ├── db.py                        # Database connection & ACID transaction manager
│   ├── schema.sql                   # Complete relational DDL schema, triggers & views
│   └── seed_data.sql                # Rich realistic restaurant initial datasets
├── database/
│   └── restaurant.db                # SQLite database file (auto-generated)
├── docs/
│   ├── 0808CS241120_dbmsReport.docx # Official formatted project report
│   ├── 0808CS241120_DBMS_PROJECT_REPORT.md # Markdown version of project report
│   └── images/                      # Generated ER diagram, class diagram, and screenshots
│       ├── er_diagram.png
│       ├── class_diagram.png
│       ├── dashboard_screenshot.png
│       ├── pos_screenshot.png
│       └── dbms_console_screenshot.png
├── assets/
│   └── ips_logo.png                 # Official IPS Academy emblem
├── build_report.py                  # Report generator script (creates .docx)
├── generate_diagrams.py             # Matplotlib diagram generator
├── generate_screenshots.py          # UI visual mockup generator
├── run.py                           # Application startup entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## 🚀 How to Run the Project

### 1. Prerequisites
- Python 3.8 or higher installed on your machine.

### 2. Install Dependencies
Open a terminal in the `DBMS` directory and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Application
Execute:
```bash
python run.py
```

### 4. Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Exploring DBMS Concepts in the App
Once the server is running, click on **"DBMS Concepts Lab"** in the top navigation bar to explore:
1. **ACID Transactions Simulator:** Select an active order and click **"Test Happy Path (COMMIT)"** or **"Simulate Failure (ROLLBACK)"** to watch step-by-step transaction processing and inventory stock updates in real time.
2. **Active Triggers & Audit Trail:** View all 5 database triggers and observe the automated audit log stream in `audit_logs`.
3. **Database Views:** Examine precomputed analytical projections (`v_daily_sales_summary`, `v_top_selling_items`, etc.).
4. **Relational Schema Dictionary:** Inspect all 12 tables, column data types, Primary Keys, Foreign Keys, and record counts.
5. **Interactive SQL Console & Optimizer:** Run queries and execute `EXPLAIN QUERY PLAN` to see B-Tree index lookups in action.

---


