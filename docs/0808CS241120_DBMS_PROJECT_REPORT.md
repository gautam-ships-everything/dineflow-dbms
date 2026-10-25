# IPS ACADEMY INDORE
## INSTITUTE OF ENGINEERING & SCIENCE
### COMPUTER SCIENCE & ENGINEERING DEPARTMENT

---

# Project Report (2026-27)
## Subject: Database Management System (DBMS)
### Project Title: **DineFlow: Intelligent Restaurant Management System & DBMS Demonstration**

**Submitted by:**
- **Name:** Gautam Soni
- **Enrollment Number:** 0808CS241120
- **Branch:** B.Tech Computer Science & Engineering
- **Institution:** IPS Academy, Indore (M.P.)

---

## TABLE OF CONTENTS
1. [CHAPTER 1: INTRODUCTION](#chapter-1-introduction)
   - 1.1 Project Overview
   - 1.2 Objectives & Goals
   - 1.3 Core DBMS Concepts Demonstrated
2. [CHAPTER 2: PROBLEM IDENTIFICATION & FEASIBILITY ANALYSIS](#chapter-2-problem-identification--feasibility-analysis)
   - 2.1 Problem Domain
   - 2.2 Solution Domain
   - 2.3 Need & Scope of the Project
   - 2.4 Platform Specification (Hardware & Software)
   - 2.5 Feasibility Analysis (Technical, Economic, Operational)
3. [CHAPTER 3: SYSTEM DESIGN & DATABASE MODELING](#chapter-3-system-design--database-modeling)
   - 3.1 Entity-Relationship (ER) Diagram & Cardinality
   - 3.2 Relational Schema & Normalization Analysis (1NF to BCNF)
   - 3.3 Class Diagram & System Architecture
   - 3.4 Application Interface & Implementation Screenshots
4. [CHAPTER 4: ADVANCED DATABASE CONCEPTS](#chapter-4-advanced-database-concepts)
   - 4.1 Automated Active Triggers & Audit Trails
   - 4.2 Analytical Database Views (Data Abstraction)
   - 4.3 ACID Transactions & Concurrency Control
   - 4.4 Indexing & Query Optimization (EXPLAIN QUERY PLAN)
5. [CHAPTER 5: CONCLUSIONS](#chapter-5-conclusions)
   - 5.1 Summary of Accomplishments
   - 5.2 Key Learning Outcomes
6. [CHAPTER 6: LIMITATIONS & FUTURE ENHANCEMENTS](#chapter-6-limitations--future-enhancements)
   - 6.1 Limitations
   - 6.2 Future Enhancements
7. [CHAPTER 7: SQL SCHEMA & IMPLEMENTATION CODE](#chapter-7-sql-schema--implementation-code)

---

## CHAPTER 1: INTRODUCTION

### 1.1 Project Overview
**DineFlow** is an enterprise-grade Restaurant Management System (RMS) designed to streamline hospitality operations while serving as a comprehensive practical demonstration of Database Management System (DBMS) concepts. Modern food service establishments manage high-speed front-of-house operations (table reservations, customer orders, Point-of-Sale billing) and back-of-house activities (kitchen order tickets, raw ingredient inventory levels, and supplier restocks). DineFlow unifies these operational facets through an automated relational database engine.

Unlike traditional CRUD applications where business rules exist solely in procedural application code, DineFlow delegates data integrity and business rules directly to the database engine. Through Primary and Foreign Key constraints with cascade actions, domain CHECK constraints, active Triggers (Event-Condition-Action model), Precomputed Analytical Views, and atomic ACID Transactions, the system delivers guaranteed data consistency, auditability, and durability.

### 1.2 Objectives & Goals
1. **Centralized Relational Storage:** Maintain organized relational records for restaurant staff, seating tables, gourmet menu offerings, customers, orders, inventory stock, and recipe mappings.
2. **Active Database Triggers:** Automate calculations (order subtotal, 5% GST, grand total) and table occupancy status updates directly within the database upon item insertion and payment completion.
3. **ACID Transaction Assurance:** Guarantee Atomicity, Consistency, Isolation, and Durability during multi-table customer checkout, coordinating bill payment, table release, loyalty point crediting, and Bill of Materials (BOM) inventory depletion.
4. **Data Abstraction via Views:** Provide virtual relational projections for business intelligence, including daily gross revenue breakdowns, top-selling dishes, table occupancy statuses, and automated low-stock warnings.
5. **Interactive DBMS Live Lab:** Incorporate a dedicated interactive console within the running application where faculty and evaluators can view schema dictionaries, trigger live ACID Commit vs Rollback scenarios, examine audit logs, and test queries with EXPLAIN QUERY PLAN index analysis.

### 1.3 Core DBMS Concepts Demonstrated
- **Relational Data Modeling:** 12 interconnected tables mapped with 1:1, 1:N, and M:N cardinalities.
- **Data Normalization:** Systematic decomposition ensuring Boyce-Codd Normal Form (BCNF), eliminating insertion, update, and deletion anomalies.
- **Referential Integrity & Constraints:** `PRIMARY KEY`, `FOREIGN KEY` (with `ON DELETE CASCADE` and `ON DELETE SET NULL`), `UNIQUE`, `NOT NULL`, and `CHECK` constraints.
- **Active Database Triggers:** Autonomous event-driven logic updating order totals, recording table transitions, and maintaining tamper-evident audit logs.
- **Transaction Processing:** Multi-statement atomic blocks (`BEGIN`, `COMMIT`, `ROLLBACK`) preventing partial state commits during complex billing and inventory deduction.
- **Query Optimization & Indexing:** Deployment of B-Tree indexes on frequent search keys (`customer_id`, `order_status`, `order_items`) and performance verification via `EXPLAIN QUERY PLAN`.

---

## CHAPTER 2: PROBLEM IDENTIFICATION & FEASIBILITY ANALYSIS

### 2.1 Problem Domain
Traditional food service environments frequently suffer from disconnected, manual, or poorly synchronized record-keeping systems. Common operational problems in restaurants include:
- **Data Redundancy & Inconsistency:** Manual handwritten order slips often mismatch the cashier's register, resulting in revenue leakage, erroneous food charges, and inaccurate tax reporting.
- **Table Seating Bottlenecks:** Waiters and hosts lack a real-time synchronized overview of table occupancy, leading to double-booking, extended customer waiting times, and under-utilized seating capacity.
- **Uncontrolled Inventory Depletion:** Kitchen staff prepare dishes without automatic stock tracking. Ingredients run out unexpectedly during peak hours because raw material consumption is disconnected from Point of Sale ordering.
- **Lack of Auditability & Integrity:** Unauthorized price adjustments or voided orders pass unnoticed without a database-level audit log recording the timestamp, previous values, and modified columns.

### 2.2 Solution Domain
DineFlow provides an integrated, automated software solution backed by a robust relational database engine:
- **Synchronized Table Management:** A live floor plan displaying real-time table statuses (Available, Occupied, Reserved) across multiple sections (Main Hall, AC Dining, Rooftop Lounge, Garden Patio, Family Cabin).
- **Automated POS & Billing:** Point of Sale interface allowing instant order assembly with automatic GST calculation and subtotal aggregation driven by database triggers.
- **Kitchen Display System (KDS):** Order tickets channeled directly to chef queues with dietary indicators (Veg, Non-Veg, Vegan) and target preparation timers.
- **Recipe Bill of Materials (BOM):** Automated inventory depletion: each menu dish is mapped to specific raw ingredient weights in the database, automatically updating stock when transactions commit.
- **Integrated DBMS Concepts Console:** An evaluation console embedded into the application permitting examiners to inspect schema metadata, execute live ACID transactions, view trigger audit records, and test queries.

### 2.3 Need & Scope
- **Need:** Real-time synchronization between front-of-house ordering and back-of-house inventory, automated tax calculation, and auditable transaction processing.
- **Scope:** Covers table reservations, menu catalog management, order assembly, kitchen order ticket tracking, inventory depletion, automated audit logging, and analytical sales reporting.

### 2.4 Platform Specification
- **Hardware Requirements:**
  - Processor: Intel Core i3 / AMD Ryzen 3 or higher (64-bit)
  - RAM: Minimum 4 GB (8 GB Recommended)
  - Storage: 500 MB free hard disk space
  - Display: 1366x768 or higher resolution
- **Software Requirements:**
  - Operating System: Microsoft Windows 10/11, Linux, or macOS
  - Programming Language: Python 3.8+ (Tested on Python 3.14)
  - Backend Framework: Flask 3.1
  - Database: SQLite 3 (Embedded ACID engine) / MariaDB compatible
  - Frontend: HTML5, CSS3, JavaScript (ES6+), FontAwesome Icons
  - Documentation Tools: Python-Docx, Matplotlib

### 2.5 Feasibility Analysis
- **Technical Feasibility:** Python and SQLite provide complete ACID transaction support, foreign key cascades, triggers, and views out of the box with zero external daemon configuration.
- **Economic Feasibility:** 100% open-source software stack with no licensing or hosting expenditure.
- **Operational Feasibility:** Web-based interface usable on desktop terminals, tablets, and mobile devices by restaurant staff with minimal training.

---

## CHAPTER 3: SYSTEM DESIGN & DATABASE MODELING

### 3.1 Entity-Relationship (ER) Diagram
The DineFlow database schema comprises 12 interconnected entities:
1. `users`: Staff credentials and role-based permissions (`Admin`, `Manager`, `Chef`, `Waiter`, `Cashier`).
2. `dining_tables`: Physical tables, capacity, sections, and live status (`Available`, `Occupied`, `Reserved`).
3. `categories`: Food and beverage categorization.
4. `menu_items`: Dish names, descriptions, prices, dietary classifications, prep times.
5. `customers`: Customer records and loyalty reward points.
6. `reservations`: Future table bookings for customers.
7. `orders`: Order header records containing subtotal, 5% GST, discounts, and grand totals.
8. `order_items`: Line items linking orders to menu items with quantities and line subtotals.
9. `payments`: Payment records capturing payment methods, transaction references, and settlement timestamps.
10. `inventory_items`: Raw material stocks, units, reorder levels, and unit costs.
11. `menu_recipes`: Bill of Materials (BOM) linking menu dishes to required ingredient quantities.
12. `audit_logs`: Automated trigger audit trail tracking all data modifications.

### 3.2 Relational Schema & Normalization Analysis
- **1NF (First Normal Form):** Every field stores atomic scalar values. No multi-valued attributes or repeating groups exist.
- **2NF (Second Normal Form):** Satisfies 1NF, and all non-key attributes are fully dependent on the entire primary key. In compound keys like `menu_recipes(item_id, ingredient_id)`, `quantity_required` depends on both keys jointly.
- **3NF (Third Normal Form):** Satisfies 2NF, with zero transitive dependencies ($X \to Y$ and $Y \to Z$). Non-key attributes depend strictly on candidate keys.
- **BCNF (Boyce-Codd Normal Form):** For every functional dependency $X \to Y$, $X$ is a superkey.

### 3.3 Class Diagram
The application follows an object-oriented architecture where model classes (`Order`, `OrderItem`, `MenuItem`, `DiningTable`, `InventoryItem`, `TransactionManager`) encapsulate state and business methods.

---

## CHAPTER 4: ADVANCED DATABASE CONCEPTS

### 4.1 Automated Active Triggers
1. `trg_order_item_after_insert`: Automatically calculates order subtotal, 5% GST, and grand total upon inserting order line items.
2. `trg_order_item_after_delete`: Recalculates order financial totals if an item is cancelled.
3. `trg_order_occupy_table`: Automatically marks a table as `Occupied` when a new Dine-In order is created.
4. `trg_payment_complete_order`: Sets order to `Completed`, marks the table as `Available`, and credits customer loyalty points upon successful payment.
5. `trg_menu_price_audit`: Captures any price updates on menu dishes into `audit_logs` with old and new values.

### 4.2 Analytical Database Views
1. `v_daily_sales_summary`: Aggregated daily metrics for completed orders, subtotal, GST collected, discounts, and gross revenue.
2. `v_top_selling_items`: Ranked menu dishes by cumulative sales quantity and revenue contribution.
3. `v_table_occupancy_status`: Real-time floor status combining table numbers, capacities, ongoing order numbers, and waiter assignments.
4. `v_low_stock_alerts`: Identifies inventory items where stock quantity is on or below reorder threshold.
5. `v_staff_performance`: Sales volume and revenue metrics achieved by waiters and staff.

### 4.3 ACID Transactions & Concurrency Control
- **Atomicity:** Checkout transaction coordinates payment insertion, order completion, table release, loyalty points update, and raw stock deduction. If any step fails, `ROLLBACK` reverts all modifications.
- **Consistency:** All table constraints (positive quantities, foreign key references, valid payment states) remain strictly valid across transaction boundaries.
- **Isolation:** SQLite transaction locks ensure that concurrent transactions do not interfere with each other.
- **Durability:** Once committed, transaction writes are durably flushed to disk.

### 4.4 Indexing & Optimization
B-Tree indexes are created on high-frequency join and search columns:
- `idx_orders_customer` on `orders(customer_id)`
- `idx_orders_table` on `orders(table_id)`
- `idx_order_items_order` on `order_items(order_id)`
- `idx_order_items_item` on `order_items(item_id)`
- `idx_menu_items_category` on `menu_items(category_id)`

Testing with `EXPLAIN QUERY PLAN` verifies that the engine uses `SEARCH TABLE ... USING INDEX` instead of linear full-table scans.

---

## CHAPTER 5: CONCLUSIONS

### 5.1 Summary
The DineFlow Restaurant Management System successfully demonstrates how foundational and advanced DBMS concepts can be engineered into a practical, real-world software system. The application handles high-throughput front-of-house ordering and back-of-house inventory operations while maintaining zero data discrepancies through database-level constraints, triggers, and transactions.

### 5.2 Key Learning Outcomes
- Advanced Relational Database Design and Normalization up to BCNF.
- Construction and debugging of active database Triggers and dynamic Views.
- Practical implementation of multi-table ACID transaction routines with automated rollback handling.
- Development of a full-stack web application integrating Python Flask with an ACID relational database.

---

## CHAPTER 6: LIMITATIONS & FUTURE ENHANCEMENTS

### 6.1 Limitations
- Operates on a single-restaurant branch scope.
- Payment gateway is implemented via database transaction logic rather than live external third-party payment APIs.
- Designed for single-node deployment (SQLite / MariaDB) rather than distributed multi-master clusters.

### 6.2 Future Enhancements
- Patron QR code self-ordering directly from smartphones.
- Machine-learning powered ingredient demand forecasting.
- Multi-branch restaurant chain synchronization and inventory transfer.
- WebSocket-based audio chimes for kitchen order ticket displays.

---

## CHAPTER 7: SQL SCHEMA & IMPLEMENTATION CODE

*(Refer to `app/schema.sql` and `app/seed_data.sql` for complete reproducible DDL and DML scripts).*

---
*Report prepared for IPS Academy Indore, Institute of Engineering & Science, CSE Department (2026-27).*
