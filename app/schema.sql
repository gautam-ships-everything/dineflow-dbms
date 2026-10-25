-- ==============================================================================
-- PROJECT: DineFlow - Intelligent Restaurant Management System
-- DEVELOPED BY: Gautam Soni (Enrollment: 0808CS241120)
-- INSTITUTION: IPS Academy, Indore - CSE Department (Session 2026-27)
-- RELATIONAL SCHEMA & DATABASE CONSTRAINTS
-- ==============================================================================

-- Enable Foreign Key constraints in SQLite
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. USERS & STAFF TABLE (Role Based Access Control: Admin, Manager, Chef, Waiter, Cashier)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS menu_recipes;
DROP TABLE IF EXISTS inventory_items;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS dining_tables;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL CHECK(role IN ('Admin', 'Manager', 'Chef', 'Waiter', 'Cashier')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 2. DINING TABLES (Table management with seating capacities and status)
-- ------------------------------------------------------------------------------
CREATE TABLE dining_tables (
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number VARCHAR(10) NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK(capacity > 0 AND capacity <= 20),
    seating_section VARCHAR(30) NOT NULL CHECK(seating_section IN ('Main Hall', 'AC Dining', 'Rooftop Lounge', 'Garden Patio', 'Family Cabin')),
    status VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK(status IN ('Available', 'Occupied', 'Reserved', 'Maintenance')),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 3. MENU CATEGORIES
-- ------------------------------------------------------------------------------
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    display_order INTEGER DEFAULT 1
);

-- ------------------------------------------------------------------------------
-- 4. MENU ITEMS
-- ------------------------------------------------------------------------------
CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
    dietary_type VARCHAR(20) NOT NULL CHECK(dietary_type IN ('Veg', 'Non-Veg', 'Vegan', 'Egg')),
    preparation_time_mins INTEGER DEFAULT 15 CHECK(preparation_time_mins > 0),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK(is_available IN (0, 1)),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ------------------------------------------------------------------------------
-- 5. CUSTOMERS (Loyalty and Contact management)
-- ------------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    loyalty_points INTEGER NOT NULL DEFAULT 0 CHECK(loyalty_points >= 0),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 6. RESERVATIONS
-- ------------------------------------------------------------------------------
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    table_id INTEGER NOT NULL,
    reservation_time DATETIME NOT NULL,
    guest_count INTEGER NOT NULL CHECK(guest_count > 0),
    special_requests TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'Confirmed' CHECK(status IN ('Confirmed', 'Seated', 'Cancelled', 'Completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (table_id) REFERENCES dining_tables(table_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------------------------
-- 7. ORDERS (Header records)
-- ------------------------------------------------------------------------------
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    table_id INTEGER,
    customer_id INTEGER,
    waiter_id INTEGER,
    order_type VARCHAR(20) NOT NULL CHECK(order_type IN ('Dine-In', 'Takeaway', 'Delivery')),
    order_status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK(order_status IN ('Active', 'In-Kitchen', 'Served', 'Billed', 'Completed', 'Cancelled')),
    subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(subtotal >= 0),
    tax_rate DECIMAL(5, 2) NOT NULL DEFAULT 5.00, -- 5% GST
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(tax_amount >= 0),
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(discount_amount >= 0),
    grand_total DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(grand_total >= 0),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES dining_tables(table_id) ON DELETE SET NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL,
    FOREIGN KEY (waiter_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- ------------------------------------------------------------------------------
-- 8. ORDER ITEMS (Line details with M:N relationship between Orders and Menu Items)
-- ------------------------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK(unit_price >= 0),
    line_total DECIMAL(10, 2) NOT NULL CHECK(line_total >= 0),
    kitchen_status VARCHAR(20) NOT NULL DEFAULT 'Queued' CHECK(kitchen_status IN ('Queued', 'Cooking', 'Ready', 'Served')),
    customization_notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------------------------
-- 9. PAYMENTS (Financial transactions)
-- ------------------------------------------------------------------------------
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL UNIQUE,
    payment_method VARCHAR(20) NOT NULL CHECK(payment_method IN ('Cash', 'Credit Card', 'Debit Card', 'UPI', 'Net Banking')),
    amount_paid DECIMAL(10, 2) NOT NULL CHECK(amount_paid > 0),
    transaction_reference VARCHAR(100),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Success' CHECK(payment_status IN ('Success', 'Pending', 'Failed', 'Refunded')),
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 10. INVENTORY ITEMS (Raw material & ingredients stock)
-- ------------------------------------------------------------------------------
CREATE TABLE inventory_items (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    stock_quantity DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK(stock_quantity >= 0),
    unit VARCHAR(20) NOT NULL, -- 'kg', 'ltr', 'packets', 'pcs'
    reorder_level DECIMAL(10, 2) NOT NULL DEFAULT 5.00,
    cost_per_unit DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    supplier_name VARCHAR(100),
    last_restocked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 11. MENU RECIPES (BOM: Bill of Materials linking Menu to Inventory Items)
-- ------------------------------------------------------------------------------
CREATE TABLE menu_recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity_required DECIMAL(10, 3) NOT NULL CHECK(quantity_required > 0),
    UNIQUE(item_id, ingredient_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES inventory_items(ingredient_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------------------------
-- 12. AUDIT LOGS (Capturing automated data audit trails via DBMS Triggers)
-- ------------------------------------------------------------------------------
CREATE TABLE audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name VARCHAR(50) NOT NULL,
    operation VARCHAR(20) NOT NULL CHECK(operation IN ('INSERT', 'UPDATE', 'DELETE', 'TRANSACTION')),
    record_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    message TEXT,
    executed_by VARCHAR(50) DEFAULT 'DBMS Trigger',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- DATABASE INDEXES FOR QUERY OPTIMIZATION (Performance Enhancement)
-- ==============================================================================
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_table ON orders(table_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_item ON order_items(item_id);
CREATE INDEX idx_reservations_time ON reservations(reservation_time);
CREATE INDEX idx_menu_items_category ON menu_items(category_id);
CREATE INDEX idx_inventory_reorder ON inventory_items(stock_quantity, reorder_level);

-- ==============================================================================
-- DATABASE VIEWS (Data Abstraction, Reporting & Encapsulation)
-- ==============================================================================

-- VIEW 1: Daily Revenue & Order Analytics Summary
CREATE VIEW v_daily_sales_summary AS
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
GROUP BY DATE(o.created_at);

-- VIEW 2: Top Selling Menu Items with Category Breakdown
CREATE VIEW v_top_selling_items AS
SELECT 
    m.item_id,
    m.name AS item_name,
    c.category_name,
    m.price,
    COALESCE(SUM(oi.quantity), 0) AS total_quantity_sold,
    COALESCE(SUM(oi.line_total), 0) AS total_revenue_generated
FROM menu_items m
JOIN categories c ON m.category_id = c.category_id
LEFT JOIN order_items oi ON m.item_id = oi.item_id
GROUP BY m.item_id, m.name, c.category_name, m.price
ORDER BY total_quantity_sold DESC;

-- VIEW 3: Live Table Occupancy & Ongoing Order Details
CREATE VIEW v_table_occupancy_status AS
SELECT 
    t.table_id,
    t.table_number,
    t.capacity,
    t.seating_section,
    t.status AS current_status,
    o.order_id AS active_order_id,
    o.order_number,
    o.order_status,
    o.grand_total,
    u.full_name AS assigned_waiter,
    o.created_at AS order_time
FROM dining_tables t
LEFT JOIN orders o ON t.table_id = o.table_id AND o.order_status NOT IN ('Completed', 'Cancelled')
LEFT JOIN users u ON o.waiter_id = u.user_id;

-- VIEW 4: Low Stock Alert View for Inventory Control
CREATE VIEW v_low_stock_alerts AS
SELECT 
    ingredient_id,
    name AS ingredient_name,
    stock_quantity,
    unit,
    reorder_level,
    ROUND(reorder_level - stock_quantity, 2) AS deficit_amount,
    supplier_name
FROM inventory_items
WHERE stock_quantity <= reorder_level
ORDER BY deficit_amount DESC;

-- VIEW 5: Waiter / Staff Sales Performance
CREATE VIEW v_staff_performance AS
SELECT 
    u.user_id,
    u.full_name AS staff_name,
    u.role,
    COUNT(o.order_id) AS total_orders_handled,
    COALESCE(SUM(o.grand_total), 0) AS total_revenue_handled
FROM users u
LEFT JOIN orders o ON u.user_id = o.waiter_id AND o.order_status = 'Completed'
WHERE u.role IN ('Waiter', 'Manager')
GROUP BY u.user_id, u.full_name, u.role;

-- ==============================================================================
-- DATABASE TRIGGERS (Automated Business Logic & Active DB Constraints)
-- ==============================================================================

-- TRIGGER 1: When an order item is added, recalculate order subtotal, tax (5%), and grand total
CREATE TRIGGER trg_order_item_after_insert
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

    -- Audit log entry
    INSERT INTO audit_logs (entity_name, operation, record_id, new_values, message)
    VALUES (
        'order_items', 
        'INSERT', 
        NEW.order_item_id, 
        json_object('order_id', NEW.order_id, 'item_id', NEW.item_id, 'qty', NEW.quantity, 'line_total', NEW.line_total),
        'Item added to order #' || NEW.order_id || '. Recalculated subtotal & tax.'
    );
END;

-- TRIGGER 2: When an order item is deleted, recalculate order totals
CREATE TRIGGER trg_order_item_after_delete
AFTER DELETE ON order_items
BEGIN
    UPDATE orders
    SET subtotal = (
        SELECT COALESCE(SUM(line_total), 0.00) 
        FROM order_items 
        WHERE order_id = OLD.order_id
    ),
    tax_amount = ROUND((
        SELECT COALESCE(SUM(line_total), 0.00) 
        FROM order_items 
        WHERE order_id = OLD.order_id
    ) * (tax_rate / 100.0), 2),
    grand_total = ROUND(
        (SELECT COALESCE(SUM(line_total), 0.00) FROM order_items WHERE order_id = OLD.order_id) +
        ((SELECT COALESCE(SUM(line_total), 0.00) FROM order_items WHERE order_id = OLD.order_id) * (tax_rate / 100.0)) -
        discount_amount, 2
    )
    WHERE order_id = OLD.order_id;

    -- Audit log entry
    INSERT INTO audit_logs (entity_name, operation, record_id, old_values, message)
    VALUES (
        'order_items', 
        'DELETE', 
        OLD.order_item_id, 
        json_object('order_id', OLD.order_id, 'item_id', OLD.item_id, 'qty', OLD.quantity),
        'Item deleted from order #' || OLD.order_id || '. Recalculated subtotal & tax.'
    );
END;

-- TRIGGER 3: When a Dine-In order is created for a table, update table status to 'Occupied'
CREATE TRIGGER trg_order_occupy_table
AFTER INSERT ON orders
WHEN NEW.table_id IS NOT NULL AND NEW.order_type = 'Dine-In'
BEGIN
    UPDATE dining_tables 
    SET status = 'Occupied', updated_at = CURRENT_TIMESTAMP
    WHERE table_id = NEW.table_id;

    INSERT INTO audit_logs (entity_name, operation, record_id, message)
    VALUES ('dining_tables', 'UPDATE', NEW.table_id, 'Table #' || NEW.table_id || ' marked Occupied due to new Order ' || NEW.order_number);
END;

-- TRIGGER 4: When a successful payment is recorded, free the table and complete order
CREATE TRIGGER trg_payment_complete_order
AFTER INSERT ON payments
WHEN NEW.payment_status = 'Success'
BEGIN
    -- Update order status to Completed
    UPDATE orders
    SET order_status = 'Completed', completed_at = CURRENT_TIMESTAMP
    WHERE order_id = NEW.order_id;

    -- Mark dining table as Available
    UPDATE dining_tables
    SET status = 'Available', updated_at = CURRENT_TIMESTAMP
    WHERE table_id = (SELECT table_id FROM orders WHERE order_id = NEW.order_id);

    -- Award loyalty points (1 point per 50 currency units spent)
    UPDATE customers
    SET loyalty_points = loyalty_points + CAST(NEW.amount_paid / 50 AS INTEGER)
    WHERE customer_id = (SELECT customer_id FROM orders WHERE order_id = NEW.order_id AND customer_id IS NOT NULL);

    -- Audit log entry
    INSERT INTO audit_logs (entity_name, operation, record_id, message)
    VALUES (
        'payments',
        'INSERT',
        NEW.payment_id,
        'Payment of ' || NEW.amount_paid || ' completed for Order #' || NEW.order_id || '. Table released and loyalty points credited.'
    );
END;

-- TRIGGER 5: Audit menu item price changes
CREATE TRIGGER trg_menu_price_audit
AFTER UPDATE OF price ON menu_items
WHEN OLD.price <> NEW.price
BEGIN
    INSERT INTO audit_logs (entity_name, operation, record_id, old_values, new_values, message)
    VALUES (
        'menu_items',
        'UPDATE',
        NEW.item_id,
        json_object('old_price', OLD.price),
        json_object('new_price', NEW.price),
        'Price updated for item: ' || NEW.name
    );
END;
