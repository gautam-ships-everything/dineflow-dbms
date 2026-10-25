import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set normal style font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Segoe UI'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    # Helper functions
    def add_title(text, size=24, color=(0x1e, 0x1b, 0x4b), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(*color)
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0x1e, 0x1b, 0x4b)
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0xea, 0x58, 0x0c)
        return p

    def add_heading3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x43, 0x38, 0xca)
        return p

    def add_p(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.18
        p.add_run(text)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix + ": ")
        r_bold.bold = True
        r_bold.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        p.add_run(text)
        return p

    def add_figure(img_path, caption, width=Inches(6.2)):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.add_run().add_picture(img_path, width=width)
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(12)
            c_run = cp.add_run(caption)
            c_run.font.size = Pt(9.5)
            c_run.font.italic = True
            c_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # -------------------------------------------------------------
    # TITLE / COVER PAGE
    # -------------------------------------------------------------
    add_title("IPS ACADEMY INDORE", 22, (0x1e, 0x1b, 0x4b), space_after=4)
    add_title("INSTITUTE OF ENGINEERING & SCIENCE\nCOMPUTER SCIENCE & ENGINEERING DEPARTMENT", 13, (0x43, 0x38, 0xca), space_after=20)

    if os.path.exists('assets/ips_logo.png'):
        add_figure('assets/ips_logo.png', "", width=Inches(1.8))

    add_title("Project Report", 15, (0x64, 0x74, 0x8b), space_after=2)
    add_title("(2026-27)", 13, (0x64, 0x74, 0x8b), space_after=14)
    add_title("Subject: Database Management System", 14, (0x0f, 0x17, 0x2a), space_after=12)
    add_title("DineFlow: Intelligent Restaurant Management System & DBMS Demonstration", 20, (0xea, 0x58, 0x0c), space_after=40)

    add_title("Submitted by:", 12, (0x64, 0x74, 0x8b), space_after=4)
    add_title("Gautam Soni\nEnrollment No: 0808CS241120\nB.Tech (Computer Science & Engineering)", 13, (0x1e, 0x1b, 0x4b), space_after=30)

    doc.add_page_break()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_heading1("TABLE OF CONTENTS")
    toc_items = [
        ("CHAPTER 1: INTRODUCTION", ["1.1 Project Overview", "1.2 Objectives & Goals", "1.3 Core DBMS Concepts Demonstrated"]),
        ("CHAPTER 2: PROBLEM IDENTIFICATION & FEASIBILITY ANALYSIS", ["2.1 Problem Domain", "2.2 Solution Domain", "2.3 Need & Scope of the Project", "2.4 Platform Specification (Hardware & Software)", "2.5 Feasibility Analysis"]),
        ("CHAPTER 3: SYSTEM DESIGN & DATABASE MODELING", ["3.1 Entity-Relationship (ER) Diagram & Cardinality", "3.2 Relational Schema & Normalization Analysis (1NF to BCNF)", "3.3 System Architecture & Class Diagram", "3.4 Application Interface & Implementation Screenshots"]),
        ("CHAPTER 4: ADVANCED DATABASE FEATURES", ["4.1 Automated Active Triggers & Audit Trails", "4.2 Analytical Database Views (Data Abstraction)", "4.3 ACID Transactions & Concurrency Control", "4.4 Indexing & Query Optimization (EXPLAIN Plan)"]),
        ("CHAPTER 5: CONCLUSIONS", ["5.1 Summary of Accomplishments", "5.2 Learning Outcomes"]),
        ("CHAPTER 6: LIMITATIONS & FUTURE ENHANCEMENTS", ["6.1 System Limitations", "6.2 Proposed Future Enhancements"]),
        ("CHAPTER 7: SQL SCHEMA & IMPLEMENTATION CODE", ["7.1 Relational Schema DDL & Constraints", "7.2 Active Database Triggers", "7.3 Precomputed Analytical Views", "7.4 Multi-Table ACID Checkout Procedure"])
    ]
    for ch, subs in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(ch)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1e, 0x1b, 0x4b)
        for s in subs:
            sp = doc.add_paragraph(style='List Bullet')
            sp.paragraph_format.space_after = Pt(2)
            sr = sp.add_run(s)
            sr.font.size = Pt(10)
            sr.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_heading1("CHAPTER 1: INTRODUCTION")
    add_heading2("1.1 Overview")
    add_p("DineFlow is an enterprise-grade Restaurant Management System (RMS) designed to streamline hospitality operations while serving as a comprehensive, end-to-end practical demonstration of Database Management System (DBMS) concepts. In the hospitality sector, operations span front-of-house table reservations, customer loyalty programs, real-time kitchen order tickets (KOT), point-of-sale (POS) billing, and back-of-house inventory raw-material tracking. DineFlow integrates all these operational facets through a unified, high-performance relational database.")
    add_p("The primary distinguishing characteristic of DineFlow is that database integrity and core business rules are strictly governed at the database engine level rather than relying entirely on application code. Through the strategic implementation of Primary and Composite Keys, Foreign Key referential integrity actions (CASCADE / RESTRICT / SET NULL), CHECK constraints, active Triggers (Event-Condition-Action model), Precomputed Views, and ACID Transaction management, the system provides a zero-compromise guarantee of data consistency, auditability, and durability.")

    add_heading2("1.2 Objectives & Goals")
    add_bullet("Centralized Relational Storage", "Maintain unified, normalized records for restaurant users, seating tables, gourmet menu offerings, customers, orders, inventory stock, and recipe mappings.")
    add_bullet("Active Database Triggers", "Automate financial computations (subtotal, 5% GST, grand totals) and table occupancy status changes instantly within SQLite / MariaDB upon item insertion and payment completion.")
    add_bullet("ACID Transaction Assurance", "Guarantee Atomicity, Consistency, Isolation, and Durability during multi-table customer checkout, coordinating bill payment, table release, loyalty point crediting, and Bill of Materials (BOM) inventory depletion.")
    add_bullet("Data Abstraction via Views", "Provide virtual relational projections for business intelligence, including daily gross revenue breakdowns, top-selling gourmet dishes, table occupancy statuses, and automated low-stock warnings.")
    add_bullet("Interactive DBMS Live Lab", "Incorporate a dedicated interactive console within the running application where faculty and evaluators can view schema dictionaries, trigger live ACID Commit vs Rollback scenarios, examine audit logs, and test queries with EXPLAIN QUERY PLAN index analysis.")

    add_heading2("1.3 Core DBMS Concepts Demonstrated")
    add_p("The DineFlow project covers the fundamental pillars of relational database engineering:")
    add_bullet("Data Modeling & Normalization", "Systematic design achieving Boyce-Codd Normal Form (BCNF), eliminating insertion, update, and deletion anomalies across 12 relational tables.")
    add_bullet("Integrity Constraints", "Enforcement of entity integrity (PRIMARY KEY), referential integrity (FOREIGN KEY with CASCADE / SET NULL), domain integrity (CHECK constraints), and uniqueness (UNIQUE keys on phone numbers, order numbers, and table codes).")
    add_bullet("Active Rules (Triggers)", "Autonomous event-driven logic updating order totals, recording table transitions, and maintaining tamper-evident audit logs.")
    add_bullet("Transaction Processing", "Multi-statement atomic blocks (BEGIN, COMMIT, ROLLBACK) preventing partial state commits during complex billing and inventory deduction.")
    add_bullet("Query Optimization & Indexing", "Deployment of B-Tree indexes on frequent search keys (customer ID, order status, order items) and performance verification via EXPLAIN QUERY PLAN.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 2: PROBLEM IDENTIFICATION & FEASIBILITY
    # -------------------------------------------------------------
    add_heading1("CHAPTER 2: PROBLEM IDENTIFICATION & FEASIBILITY ANALYSIS")
    add_heading2("2.1 Problem Domain")
    add_p("Traditional food service environments frequently suffer from disconnected, manual, or poorly synchronized record-keeping systems. Common operational problems in restaurants include:")
    add_bullet("Data Redundancy & Inconsistency", "Manual handwritten order slips often mismatch the cashier's register, resulting in revenue leakage, erroneous food charges, and inaccurate tax reporting.")
    add_bullet("Table Seating Bottlenecks", "Waiters and hosts lack a real-time synchronized overview of table occupancy, leading to double-booking, extended customer waiting times, and under-utilized seating capacity.")
    add_bullet("Uncontrolled Inventory Depletion", "Kitchen staff prepare dishes without automatic stock tracking. Ingredients run out unexpectedly during peak hours because raw material consumption is disconnected from Point of Sale ordering.")
    add_bullet("Lack of Auditability & Integrity", "Unauthorized price adjustments or voided orders pass unnoticed without a database-level audit log recording the timestamp, previous values, and modified columns.")

    add_heading2("2.2 Solution Domain")
    add_p("DineFlow provides an integrated, automated software solution backed by a robust relational database engine:")
    add_bullet("Synchronized Table Management", "A live floor plan displaying real-time table statuses (Available, Occupied, Reserved) across multiple sections (Main Hall, AC Dining, Rooftop Lounge, Garden Patio, Family Cabin).")
    add_bullet("Automated POS & Billing", "Point of Sale interface allowing instant order assembly with automatic GST calculation and subtotal aggregation driven by database triggers.")
    add_bullet("Kitchen Display System (KDS)", "Order tickets channeled directly to chef queues with dietary indicators (Veg, Non-Veg, Vegan) and target preparation timers.")
    add_bullet("Recipe Bill of Materials (BOM)", "Automated inventory depletion: each menu dish is mapped to specific raw ingredient weights in the database, automatically updating stock when transactions commit.")
    add_bullet("Integrated DBMS Concepts Console", "An evaluation console embedded into the application permitting examiners to inspect schema metadata, execute live ACID transactions, view trigger audit records, and test queries.")

    add_heading2("2.3 Need & Scope")
    add_p("The scope of DineFlow encompasses the full operational lifecycle of a modern dine-in and takeaway restaurant, coupled with pedagogical database demonstrations:")
    add_bullet("Role-Based User Security", "Authentication and access profiles for Administrators, Managers, Chefs, Waiters, and Cashiers.")
    add_bullet("Customer Relationship & Loyalty", "Automated points accrual based on order value (1 point per Rs. 50 spent) stored persistently in customer profiles.")
    add_bullet("Performance Optimization", "Pre-configured B-Tree indexes and materialized views designed to scale smoothly as transaction volumes grow.")

    add_heading2("2.4 Platform Specification")
    add_p("The following hardware and software specifications were utilized for designing, developing, and executing the DineFlow system:")

    # Table of Specifications
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].text = "Component"
    hdr[1].text = "Development Environment"
    hdr[2].text = "Minimum Requirement"
    for c in hdr:
        set_cell_background(c, "1E1B4B")
        for p in c.paragraphs:
            p.runs[0].font.color.rgb = RGBColor(0xff, 0xff, 0xff)
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(9.5)

    specs = [
        ("Processor", "Intel Core i5 / AMD Ryzen 5 or higher", "Intel Core i3 (64-bit)"),
        ("System RAM", "8 GB / 16 GB DDR4", "4 GB RAM"),
        ("Operating System", "Microsoft Windows 11 / 10 (64-bit)", "Windows / Linux / macOS"),
        ("Programming Language", "Python 3.14 / 3.11", "Python 3.8+"),
        ("Backend Framework", "Flask 3.1 (WSGI Web Framework)", "Flask / Jinja2"),
        ("Database Engine", "SQLite 3 (Embedded ACID Engine) / MariaDB", "SQLite 3 / MariaDB / MySQL"),
        ("Frontend Technologies", "HTML5, CSS3 Glassmorphism, JavaScript (ES6+)", "Modern Web Browser"),
        ("Code Editor & Tools", "Visual Studio Code, Python-Docx, Matplotlib", "Any Code Editor")
    ]
    for row_data in specs:
        row = table.add_row().cells
        for idx, val in enumerate(row_data):
            row[idx].text = val
            set_cell_background(row[idx], "F8FAFC" if specs.index(row_data)%2==0 else "FFFFFF")
            for p in row[idx].paragraphs:
                p.runs[0].font.size = Pt(9)
                set_cell_margins(row[idx], top=80, bottom=80, left=100, right=100)

    add_heading2("2.5 Feasibility Analysis")
    add_bullet("Technical Feasibility", "Python's built-in sqlite3 engine provides enterprise-standard ACID compliance, foreign keys, triggers, and views without demanding complex server administration. The web interface operates smoothly on any browser.")
    add_bullet("Economic Feasibility", "Constructed completely using free, open-source software libraries (Python, Flask, SQLite, FontAwesome). Zero licensing costs are incurred.")
    add_bullet("Operational Feasibility", "The intuitive graphical user interface allows restaurant servers and kitchen staff to manage tables, place orders, and track preparation statuses with minimal training.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 3: SYSTEM DESIGN & DATABASE MODELING
    # -------------------------------------------------------------
    add_heading1("CHAPTER 3: SYSTEM DESIGN & DATABASE MODELING")
    add_heading2("3.1 Entity-Relationship (ER) Diagram")
    add_p("The Entity-Relationship model serves as the conceptual blueprint of the DineFlow database. It defines the core real-world entities, their distinct attributes, key identifiers, and structural relationships (cardinalities).")
    add_p("The DineFlow database comprises 12 interconnected relational entities:")
    add_bullet("USERS", "Stores staff accounts with role-based access levels (Admin, Manager, Chef, Waiter, Cashier).")
    add_bullet("DINING_TABLES", "Stores restaurant seating inventory with table numbers, seating capacities, locations, and live occupancy statuses.")
    add_bullet("CATEGORIES", "Organizes food items into logical sections (Appetizers, Main Course, Breads & Rice, Desserts, Beverages).")
    add_bullet("MENU_ITEMS", "Contains food catalog offerings with prices, dietary tags, preparation times, and availability flags.")
    add_bullet("CUSTOMERS", "Tracks client records, unique telephone numbers, email addresses, and accumulated loyalty rewards points.")
    add_bullet("RESERVATIONS", "Connects customers with dining tables for scheduled future bookings.")
    add_bullet("ORDERS", "Header records for dining transactions containing unique order numbers, assigned waiter, table, timestamps, subtotal, 5% GST, and grand total.")
    add_bullet("ORDER_ITEMS", "Child line items resolving the Many-to-Many relationship between Orders and Menu Items.")
    add_bullet("PAYMENTS", "Financial settlement entity capturing payment modes (UPI, Card, Cash), transaction references, and completion status.")
    add_bullet("INVENTORY_ITEMS", "Manages raw materials, stock quantities, units of measure (kg, ltr), reorder thresholds, and suppliers.")
    add_bullet("MENU_RECIPES (BOM)", "Resolves the Many-to-Many relationship between Menu Offerings and Inventory Ingredients to automate ingredient consumption.")
    add_bullet("AUDIT_LOGS", "Captures automated database trigger audit trails recording entity names, operations (INSERT, UPDATE, DELETE), and modification payloads.")

    add_figure('docs/images/er_diagram.png', "Figure 3.1: Complete Entity-Relationship (ER) Diagram of DineFlow RMS")

    add_heading2("3.2 Relational Schema & Normalization Analysis")
    add_p("Database normalization is the formal process of structuring relational schema attributes to minimize data redundancy and prevent insertion, update, and deletion anomalies. DineFlow satisfies 3NF and BCNF standards:")
    add_bullet("First Normal Form (1NF)", "All table attributes contain strictly atomic (indivisible) scalar values. Repeating groups and multi-valued arrays are entirely decoupled into distinct tables (e.g. order items are stored in individual rows of order_items rather than a comma-delimited list in orders).")
    add_bullet("Second Normal Form (2NF)", "The schema satisfies 1NF and guarantees that every non-prime attribute is fully functionally dependent on the complete candidate key. In bridge tables like menu_recipes(item_id, ingredient_id), the attribute quantity_required depends on both keys jointly.")
    add_bullet("Third Normal Form (3NF)", "The schema satisfies 2NF and exhibits zero transitive dependencies (X -> Y and Y -> Z where non-key attributes determine other non-key attributes). For instance, customer contact details are stored strictly in customers; orders merely references customer_id via Foreign Key rather than duplicating customer phone and email.")
    add_bullet("Boyce-Codd Normal Form (BCNF)", "For every non-trivial functional dependency X -> Y, X is a superkey of the respective relation, ensuring optimal integrity.")

    add_heading2("3.3 System Architecture & Class Diagram")
    add_p("The class diagram models the object-oriented structure of the backend application, highlighting data encapsulation, attributes, and business operations.")
    add_figure('docs/images/class_diagram.png', "Figure 3.2: Object Class Diagram and Logical Domain Architecture")

    add_heading2("3.4 Application Interface & Implementation Screenshots")
    add_p("The DineFlow application offers a responsive, glassmorphic graphical user interface built with HTML5, CSS3, JavaScript, and Jinja2 templating, running on the Flask micro-framework.")

    add_heading3("1. Executive Operations Dashboard")
    add_p("The dashboard provides live operational visibility: real-time gross revenue counters, table occupancy counts, active kitchen order queues, low-stock ingredient alerts, a dynamic floor plan, and recent trigger audit activity.")
    add_figure('docs/images/dashboard_screenshot.png', "Figure 3.3: Operations Dashboard with Live Floorplan and Trigger Audit Stream")

    add_heading3("2. Point of Sale (POS) & Automated Billing Interface")
    add_p("The Point of Sale interface facilitates rapid order taking. Servers select menu items into an interactive cart. When the order is placed, the database trigger trg_order_item_after_insert computes subtotal and GST automatically, while trg_order_occupy_table sets the table to 'Occupied'.")
    add_figure('docs/images/pos_screenshot.png', "Figure 3.4: Point of Sale Interface with Dynamic Trigger-Calculated Billing")

    add_heading3("3. DBMS Concepts Live Demonstration Console")
    add_p("A specialized live lab interface embedded directly into the application allowing evaluators to simulate atomic ACID checkout transactions (testing COMMIT vs ROLLBACK), inspect active triggers, examine precomputed analytical views, and run arbitrary SELECT queries with EXPLAIN QUERY PLAN index verification.")
    add_figure('docs/images/dbms_console_screenshot.png', "Figure 3.5: Interactive DBMS Concepts Demonstration Console")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 4: ADVANCED DATABASE FEATURES
    # -------------------------------------------------------------
    add_heading1("CHAPTER 4: ADVANCED DATABASE FEATURES & IMPLEMENTATION")
    
    add_heading2("4.1 Automated Active Triggers & Audit Trails")
    add_p("Triggers are stored database procedures that automatically execute in response to specified Data Manipulation Language (DML) events (INSERT, UPDATE, DELETE). DineFlow implements 5 production-grade triggers:")
    add_bullet("trg_order_item_after_insert", "Fired AFTER INSERT ON order_items. Automatically recalculates orders.subtotal, orders.tax_amount (5% GST), and orders.grand_total, and inserts an audit log entry.")
    add_bullet("trg_order_item_after_delete", "Fired AFTER DELETE ON order_items. Automatically adjusts subtotal and tax downwards upon item cancellation.")
    add_bullet("trg_order_occupy_table", "Fired AFTER INSERT ON orders when order_type = 'Dine-In'. Automatically transitions dining_tables.status to 'Occupied'.")
    add_bullet("trg_payment_complete_order", "Fired AFTER INSERT ON payments when payment_status = 'Success'. Automatically completes the order, releases dining_tables.status back to 'Available', and awards loyalty points to the customer.")
    add_bullet("trg_menu_price_audit", "Fired AFTER UPDATE OF price ON menu_items. Automatically logs the previous price, new price, and timestamp into audit_logs.")

    add_heading2("4.2 Analytical Database Views (Data Abstraction)")
    add_p("Views encapsulate complex multi-table SQL queries, presenting simplified virtual tables for analytical reporting:")
    add_bullet("v_daily_sales_summary", "Aggregates daily completed orders, food subtotal, total GST collected, total discounts, and gross revenue.")
    add_bullet("v_top_selling_items", "Ranks menu dishes across categories by cumulative quantity sold and gross revenue generated.")
    add_bullet("v_table_occupancy_status", "Combines dining tables with active order numbers, waiter assignments, and order totals into a live floor summary.")
    add_bullet("v_low_stock_alerts", "Filters inventory ingredients whose stock levels have fallen below the predefined reorder threshold.")
    add_bullet("v_staff_performance", "Aggregates orders handled and total revenue generated per waiter and manager.")

    add_heading2("4.3 ACID Transactions & Concurrency Control")
    add_p("The DineFlow checkout workflow illustrates the four ACID guarantees:")
    add_bullet("Atomicity (All-or-Nothing)", "Checkout involves: (a) payment insertion, (b) recipe-based inventory stock deduction, (c) order completion, (d) table release, and (e) loyalty point awards. If any error or simulated failure occurs, all intermediate operations are rolled back completely via ROLLBACK TRANSACTION.")
    add_bullet("Consistency", "State transitions strictly uphold database constraints (e.g. stock quantities cannot violate CHECK(stock_quantity >= 0), foreign keys remain valid).")
    add_bullet("Isolation", "Database locking mechanisms ensure concurrent transactions cannot read dirty or uncommitted checkout states.")
    add_bullet("Durability", "Once COMMIT is executed, transaction results are written to non-volatile disk storage, surviving unexpected system crashes.")

    add_heading2("4.4 Indexing & Query Optimization")
    add_p("B-Tree indexes were constructed on foreign keys and frequently searched attributes to eliminate expensive table scans: idx_orders_customer, idx_orders_table, idx_order_items_order, idx_order_items_item, and idx_menu_items_category. Verifying queries with EXPLAIN QUERY PLAN demonstrates that the query planner performs direct SEARCH TABLE USING INDEX lookups in O(log N) logarithmic time.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 5: CONCLUSIONS
    # -------------------------------------------------------------
    add_heading1("CHAPTER 5: CONCLUSIONS")
    add_heading2("5.1 Summary of Accomplishments")
    add_p("The DineFlow project successfully demonstrates the end-to-end conception, relational modeling, implementation, and deployment of a modern Restaurant Management System. By grounding the architecture in relational theory and DBMS mechanisms, the project guarantees high operational reliability, financial accuracy, and data consistency.")
    add_p("The project bridges theoretical concepts taught in the Database Management System curriculum with practical software engineering, proving that active database mechanisms (triggers, foreign keys, views, indexes, ACID transactions) dramatically reduce application code complexity while guaranteeing bulletproof data integrity.")

    add_heading2("5.2 Learning Outcomes")
    add_bullet("Advanced Schema Normalization", "Gained practical mastery in applying 1NF, 2NF, 3NF, and BCNF normalization rules to complex multi-entity domains.")
    add_bullet("Active Database Triggers", "Developed hands-on proficiency in authoring event-condition-action triggers that autonomously calculate bills and track audit logs.")
    add_bullet("Transactional Integrity", "Implemented robust transaction rollback handlers safeguarding multi-table mutations against sudden operational failures.")
    add_bullet("Full-Stack Web Integration", "Seamlessly connected a Python Flask backend to a relational database engine, rendering responsive user interfaces.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 6: LIMITATIONS & FUTURE ENHANCEMENTS
    # -------------------------------------------------------------
    add_heading1("CHAPTER 6: LIMITATIONS & FUTURE ENHANCEMENTS")
    add_heading2("6.1 System Limitations")
    add_bullet("Single-Location Scope", "The current database design is optimized for a single restaurant branch rather than a multi-branch franchise with cross-store inventory transfers.")
    add_bullet("Local Gateway Simulation", "Online UPI and card transactions are simulated through database transaction logic rather than live production payment gateways (e.g. Razorpay/Stripe APIs).")
    add_bullet("Simulated Concurrency", "While SQLite supports WAL (Write-Ahead Logging) and robust ACID transactions, high-concurrency enterprise installations with hundreds of simultaneous terminals benefit from distributed servers such as PostgreSQL or MariaDB Galera Cluster.")

    add_heading2("6.2 Proposed Future Enhancements")
    add_bullet("Customer Self-Service QR Ordering", "Enable patrons to scan dynamic table QR codes to view the digital menu and submit orders directly into the database queue.")
    add_bullet("Predictive AI Inventory Forecasting", "Integrate machine learning models to analyze historical order trends from v_daily_sales_summary to predict upcoming weekly ingredient reorder quantities.")
    add_bullet("Multi-Outlet Franchise Replication", "Expand relational schema with branch_id foreign keys and implement master-replica database replication across geographic restaurant chains.")
    add_bullet("Kitchen Audio & KDS Touch Displays", "Add WebSocket notifications for real-time acoustic chimes when new tickets land in the kitchen queue.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 7: SQL SCHEMA & IMPLEMENTATION CODE
    # -------------------------------------------------------------
    add_heading1("CHAPTER 7: SQL SCHEMA & IMPLEMENTATION CODE")
    add_heading2("7.1 Relational Schema DDL & Constraints")
    add_p("Below is the core Data Definition Language (DDL) establishing the relational schema, constraints, and tables in the DineFlow database:")

    schema_sql_sample = """CREATE TABLE dining_tables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number VARCHAR(10) NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK(capacity > 0 AND capacity <= 20),
    seating_section VARCHAR(30) NOT NULL CHECK(seating_section IN ('Main Hall', 'AC Dining', 'Rooftop Lounge', 'Garden Patio', 'Family Cabin')),
    status VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK(status IN ('Available', 'Occupied', 'Reserved', 'Maintenance')),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    table_id INTEGER,
    customer_id INTEGER,
    waiter_id INTEGER,
    order_type VARCHAR(20) NOT NULL CHECK(order_type IN ('Dine-In', 'Takeaway', 'Delivery')),
    order_status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK(order_status IN ('Active', 'In-Kitchen', 'Served', 'Billed', 'Completed', 'Cancelled')),
    subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(subtotal >= 0),
    tax_rate DECIMAL(5, 2) NOT NULL DEFAULT 5.00,
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(tax_amount >= 0),
    grand_total DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(grand_total >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES dining_tables(table_id) ON DELETE SET NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL,
    FOREIGN KEY (waiter_id) REFERENCES users(user_id) ON DELETE SET NULL
);"""

    p = doc.add_paragraph()
    r = p.add_run(schema_sql_sample)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    add_heading2("7.2 Active Database Triggers")
    trigger_sql_sample = """CREATE TRIGGER trg_order_item_after_insert
AFTER INSERT ON order_items
BEGIN
    UPDATE orders
    SET subtotal = (
        SELECT COALESCE(SUM(line_total), 0.00) 
        FROM order_items 
        WHERE order_id = NEW.order_id
    ),
    tax_amount = ROUND((
        SELECT COALESCE(SUM(line_total), 0.00) 
        FROM order_items 
        WHERE order_id = NEW.order_id
    ) * (tax_rate / 100.0), 2),
    grand_total = ROUND(
        (SELECT COALESCE(SUM(line_total), 0.00) FROM order_items WHERE order_id = NEW.order_id) +
        ((SELECT COALESCE(SUM(line_total), 0.00) FROM order_items WHERE order_id = NEW.order_id) * (tax_rate / 100.0)) -
        discount_amount, 2
    )
    WHERE order_id = NEW.order_id;

    INSERT INTO audit_logs (entity_name, operation, record_id, message)
    VALUES ('order_items', 'INSERT', NEW.order_item_id, 'Added item to order #' || NEW.order_id || '. Recalculated subtotal & GST.');
END;"""

    p = doc.add_paragraph()
    r = p.add_run(trigger_sql_sample)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    add_heading2("7.3 Analytical Database Views")
    views_sql_sample = """CREATE VIEW v_daily_sales_summary AS
SELECT 
    DATE(o.created_at) AS sale_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.subtotal), 0) AS total_subtotal,
    COALESCE(SUM(o.tax_amount), 0) AS total_tax,
    COALESCE(SUM(o.discount_amount), 0) AS total_discount,
    COALESCE(SUM(o.grand_total), 0) AS gross_revenue,
    COALESCE(ROUND(AVG(o.grand_total), 2), 0) AS average_order_value
FROM orders o
WHERE o.order_status IN ('Completed', 'Billed')
GROUP BY DATE(o.created_at);"""

    p = doc.add_paragraph()
    r = p.add_run(views_sql_sample)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    # Save to both target locations
    out1 = 'docs/0808CS241120_dbmsReport.docx'
    out2 = '../docs/0808CS241120_dbmsReport.docx'
    doc.save(out1)
    doc.save(out2)
    print(f"Report saved successfully to {out1} and {out2}")

if __name__ == '__main__':
    create_report()
