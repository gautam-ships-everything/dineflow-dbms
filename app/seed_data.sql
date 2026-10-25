-- ==============================================================================
-- PROJECT: DineFlow - Intelligent Restaurant Management System
-- DEVELOPED BY: Gautam Soni (Enrollment: 0808CS241120)
-- SEED DATA: Realistic initial datasets for restaurant operations
-- ==============================================================================

-- 1. USERS (Password hashed with sha256 or mock tokens)
INSERT INTO users (username, password_hash, full_name, email, phone, role) VALUES
('admin', 'pbkdf2:sha256:admin123', 'Gautam Soni (Administrator)', 'admin@dineflow.local', '9876543210', 'Admin'),
('manager_rohit', 'pbkdf2:sha256:manager123', 'Rohit Sharma', 'rohit@dineflow.local', '9876543211', 'Manager'),
('chef_sanjay', 'pbkdf2:sha256:chef123', 'Sanjay Kapoor', 'chef@dineflow.local', '9876543212', 'Chef'),
('waiter_anil', 'pbkdf2:sha256:waiter123', 'Anil Verma', 'anil@dineflow.local', '9876543213', 'Waiter'),
('waiter_priya', 'pbkdf2:sha256:waiter123', 'Priya Patel', 'priya@dineflow.local', '9876543214', 'Waiter'),
('cashier_sunil', 'pbkdf2:sha256:cashier123', 'Sunil Joshi', 'sunil@dineflow.local', '9876543215', 'Cashier');

-- 2. DINING TABLES
INSERT INTO dining_tables (table_number, capacity, seating_section, status) VALUES
('T-01', 2, 'Main Hall', 'Available'),
('T-02', 4, 'Main Hall', 'Available'),
('T-03', 4, 'Main Hall', 'Available'),
('T-04', 6, 'Main Hall', 'Available'),
('AC-01', 4, 'AC Dining', 'Available'),
('AC-02', 4, 'AC Dining', 'Available'),
('AC-03', 8, 'AC Dining', 'Available'),
('RT-01', 2, 'Rooftop Lounge', 'Available'),
('RT-02', 4, 'Rooftop Lounge', 'Available'),
('GP-01', 4, 'Garden Patio', 'Available'),
('GP-02', 6, 'Garden Patio', 'Available'),
('VIP-01', 10, 'Family Cabin', 'Available');

-- 3. CATEGORIES
INSERT INTO categories (category_name, description, display_order) VALUES
('Appetizers & Starters', 'Crispy, savory snacks and starters to kick off your dining experience.', 1),
('Main Course', 'Rich aromatic curries, traditional delicacies and chef specialties.', 2),
('Breads & Rice', 'Freshly baked tandoori breads, basmati biryanis and pulao.', 3),
('Desserts', 'Decadent sweet delights, traditional Indian desserts and gelatos.', 4),
('Beverages', 'Chilled mocktails, shakes, freshly brewed tea and artisanal coffees.', 5);

-- 4. MENU ITEMS
INSERT INTO menu_items (category_id, name, description, price, dietary_type, preparation_time_mins, is_available) VALUES
-- Starters
(1, 'Paneer Tikka Sunhari', 'Cottage cheese cubes marinated in saffron yogurt and char-grilled.', 280.00, 'Veg', 15, 1),
(1, 'Crispy Corn & Waterchestnut', 'Golden fried sweet corn tossed in crushed pepper and fresh herbs.', 240.00, 'Veg', 12, 1),
(1, 'Murgh Malai Tikka', 'Tender chicken morsels steeped in cream, cardamom and cheese.', 340.00, 'Non-Veg', 18, 1),
(1, 'Hara Bhara Kebab', 'Spinach, green peas and spice patties shallow fried to perfection.', 220.00, 'Vegan', 10, 1),
-- Main Course
(2, 'Paneer Butter Masala', 'Fresh cottage cheese simmered in a silky tomato butter gravy with fenugreek.', 320.00, 'Veg', 15, 1),
(2, 'Dal Makhani Heritage', 'Slow cooked black lentils with churned butter and royal spices overnight.', 260.00, 'Veg', 12, 1),
(2, 'Butter Chicken Delhi Style', 'Smoked shredded tandoori chicken cooked in velvety tomato cream gravy.', 390.00, 'Non-Veg', 20, 1),
(2, 'Subz Handi Dum', 'Melange of fresh garden vegetables braised with fragrant spices in clay pot.', 290.00, 'Vegan', 15, 1),
-- Breads & Rice
(3, 'Garlic Butter Naan', 'Clay oven leavened bread brushed with garlic butter and fresh coriander.', 75.00, 'Veg', 8, 1),
(3, 'Dum Biryani Awadhi (Veg)', 'Fragrant basmati rice layered with vegetables, saffron and kewra.', 280.00, 'Veg', 20, 1),
(3, 'Dum Biryani Lucknowi (Murgh)', 'Classic spiced chicken biryani cooked on slow flame with whole spices.', 360.00, 'Non-Veg', 25, 1),
(3, 'Tandoori Roti Butter', 'Stone ground whole wheat flatbread made fresh in tandoor.', 35.00, 'Vegan', 5, 1),
-- Desserts
(4, 'Gulab Jamun with Rabri', 'Warm khoya dumplings soaked in rose syrup served with reduced rabri.', 140.00, 'Veg', 5, 1),
(4, 'Sizzling Brownie with Ice Cream', 'Fudgy walnut brownie topped with vanilla bean ice cream & hot fudge.', 190.00, 'Veg', 8, 1),
-- Beverages
(5, 'Masala Chaas & Mint', 'Spiced buttermilk churned with roasted cumin, mint and rock salt.', 80.00, 'Veg', 5, 1),
(5, 'Blue Lagoon Mocktail', 'Curacao blend with lime, sprite, crushed mint and sea salt.', 150.00, 'Vegan', 5, 1),
(5, 'Kesar Pista Lassi', 'Thick sweetened curd blended with saffron strands and pistachios.', 120.00, 'Veg', 5, 1);

-- 5. CUSTOMERS
INSERT INTO customers (name, phone, email, loyalty_points) VALUES
('Vikramaditya Rao', '9826011122', 'vikram.rao@example.com', 45),
('Ananya Deshmukh', '9826033344', 'ananya.d@example.com', 80),
('Rohan Singhal', '9826055566', 'rohan.singhal@example.com', 120),
('Meera Nambiar', '9826077788', 'meera.n@example.com', 25),
('Kavita Verma', '9826099900', 'kavita.v@example.com', 60);

-- 6. INVENTORY ITEMS (Raw Ingredients)
INSERT INTO inventory_items (name, stock_quantity, unit, reorder_level, cost_per_unit, supplier_name) VALUES
('Fresh Paneer (Cottage Cheese)', 18.50, 'kg', 5.00, 320.00, 'Amul Fresh Dairy Indore'),
('Chicken Breast Boneless', 24.00, 'kg', 8.00, 260.00, 'Supreme Poultry Suppliers'),
('Basmati Rice (Dehradun)', 50.00, 'kg', 15.00, 95.00, 'Agro Foodgrains Corp'),
('Black Urad Lentils', 30.00, 'kg', 10.00, 110.00, 'Madhya Bharat Pulses'),
('Tomatoes (Grade A)', 40.00, 'kg', 10.00, 35.00, 'Choithram Mandi Traders'),
('Dairy Butter & Cream', 12.00, 'kg', 4.00, 480.00, 'Sanchi Dairy Federation'),
('Garlic & Ginger Puree', 8.00, 'kg', 3.00, 140.00, 'Choithram Mandi Traders'),
('Refined Wheat Flour (Maida)', 45.00, 'kg', 12.00, 40.00, 'Malwa Milling Co'),
('Cooking Oil (Sunflower)', 35.00, 'ltr', 10.00, 130.00, 'Fortune Edible Oils'),
('Saffron & Royal Spices', 0.85, 'kg', 1.00, 8500.00, 'Kashmir Herb & Spice Hub'); -- Note: Below reorder level to trigger alert view!

-- 7. MENU RECIPES (Bill of Materials linking Menu to Inventory)
INSERT INTO menu_recipes (item_id, ingredient_id, quantity_required) VALUES
(1, 1, 0.200), -- Paneer Tikka uses 200g Paneer
(1, 6, 0.050), -- Paneer Tikka uses 50g Cream
(3, 2, 0.250), -- Murgh Malai Tikka uses 250g Chicken
(3, 6, 0.060), -- Murgh Malai Tikka uses 60g Cream
(5, 1, 0.220), -- Paneer Butter Masala uses 220g Paneer
(5, 5, 0.150), -- Paneer Butter Masala uses 150g Tomato
(5, 6, 0.080), -- Paneer Butter Masala uses 80g Butter
(6, 4, 0.150), -- Dal Makhani uses 150g Lentils
(6, 6, 0.075), -- Dal Makhani uses 75g Butter
(7, 2, 0.250), -- Butter Chicken uses 250g Chicken
(7, 5, 0.150), -- Butter Chicken uses 150g Tomato
(7, 6, 0.080), -- Butter Chicken uses 80g Butter
(9, 8, 0.120), -- Garlic Naan uses 120g Maida
(9, 6, 0.025), -- Garlic Naan uses 25g Butter
(10, 3, 0.180), -- Veg Biryani uses 180g Rice
(11, 3, 0.180), -- Chicken Biryani uses 180g Rice
(11, 2, 0.200); -- Chicken Biryani uses 200g Chicken

-- 8. INITIAL COMPLETED ORDERS & PAYMENTS (For historical reports & views)
-- Order 1: Table T-01
INSERT INTO orders (order_number, table_id, customer_id, waiter_id, order_type, order_status, subtotal, tax_amount, discount_amount, grand_total, created_at, completed_at)
VALUES ('ORD-2026-1001', 1, 1, 4, 'Dine-In', 'Completed', 675.00, 33.75, 0.00, 708.75, datetime('now', '-2 days'), datetime('now', '-2 days', '+45 minutes'));

INSERT INTO order_items (order_id, item_id, quantity, unit_price, line_total, kitchen_status) VALUES
(1, 1, 1, 280.00, 280.00, 'Served'),
(1, 5, 1, 320.00, 320.00, 'Served'),
(1, 9, 1, 75.00, 75.00, 'Served');

INSERT INTO payments (order_id, payment_method, amount_paid, transaction_reference, payment_status, payment_time)
VALUES (1, 'UPI', 708.75, 'UPI/20261023/889201', 'Success', datetime('now', '-2 days', '+45 minutes'));

-- Order 2: Table AC-01
INSERT INTO orders (order_number, table_id, customer_id, waiter_id, order_type, order_status, subtotal, tax_amount, discount_amount, grand_total, created_at, completed_at)
VALUES ('ORD-2026-1002', 5, 2, 5, 'Dine-In', 'Completed', 1070.00, 53.50, 50.00, 1073.50, datetime('now', '-1 days'), datetime('now', '-1 days', '+50 minutes'));

INSERT INTO order_items (order_id, item_id, quantity, unit_price, line_total, kitchen_status) VALUES
(2, 3, 1, 340.00, 340.00, 'Served'),
(2, 7, 1, 390.00, 390.00, 'Served'),
(2, 9, 2, 75.00, 150.00, 'Served'),
(2, 14, 1, 190.00, 190.00, 'Served');

INSERT INTO payments (order_id, payment_method, amount_paid, transaction_reference, payment_status, payment_time)
VALUES (2, 'Credit Card', 1073.50, 'TXN-CC-990142', 'Success', datetime('now', '-1 days', '+50 minutes'));

-- 9. ACTIVE ORDERS & TABLE OCCUPANCY (For live POS & Kitchen demo)
INSERT INTO orders (order_number, table_id, customer_id, waiter_id, order_type, order_status, subtotal, tax_amount, discount_amount, grand_total, created_at)
VALUES ('ORD-2026-1003', 2, 3, 4, 'Dine-In', 'In-Kitchen', 840.00, 42.00, 0.00, 882.00, datetime('now', '-15 minutes'));

INSERT INTO order_items (order_id, item_id, quantity, unit_price, line_total, kitchen_status) VALUES
(3, 1, 1, 280.00, 280.00, 'Cooking'),
(3, 6, 1, 260.00, 260.00, 'Queued'),
(3, 10, 1, 280.00, 280.00, 'Cooking'),
(3, 16, 2, 150.00, 300.00, 'Ready');

UPDATE dining_tables SET status = 'Occupied' WHERE table_id = 2;

-- 10. RESERVATIONS
INSERT INTO reservations (customer_id, table_id, reservation_time, guest_count, special_requests, status) VALUES
(4, 8, datetime('now', '+2 hours'), 2, 'Window table, celebrating anniversary', 'Confirmed'),
(5, 12, datetime('now', '+5 hours'), 8, 'Family get-together, require high chair for toddler', 'Confirmed');

UPDATE dining_tables SET status = 'Reserved' WHERE table_id IN (8, 12);
