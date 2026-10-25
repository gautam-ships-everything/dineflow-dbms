import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from app.db import get_db_connection, execute_query, execute_acid_transaction, init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dineflow-secret-key-cse-2026'

    # Ensure DB is created
    init_db()

    @app.route('/')
    def index():
        conn = get_db_connection()
        cur = conn.cursor()

        # Stats
        total_revenue = cur.execute("SELECT COALESCE(SUM(amount_paid), 0) FROM payments WHERE payment_status = 'Success'").fetchone()[0]
        total_orders = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        active_tables = cur.execute("SELECT COUNT(*) FROM dining_tables WHERE status = 'Occupied'").fetchone()[0]
        total_tables = cur.execute("SELECT COUNT(*) FROM dining_tables").fetchone()[0]
        low_stock_count = cur.execute("SELECT COUNT(*) FROM inventory_items WHERE stock_quantity <= reorder_level").fetchone()[0]

        # Recent Orders
        recent_orders = cur.execute("""
            SELECT o.order_id, o.order_number, o.order_type, o.order_status, o.grand_total, o.created_at,
                   t.table_number, c.name AS customer_name
            FROM orders o
            LEFT JOIN dining_tables t ON o.table_id = t.table_id
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY o.created_at DESC LIMIT 5
        """).fetchall()

        # Table status list
        tables = cur.execute("SELECT * FROM v_table_occupancy_status").fetchall()

        # Recent Audit logs
        audit_logs = cur.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 6").fetchall()

        conn.close()
        return render_template('index.html',
                               total_revenue=total_revenue,
                               total_orders=total_orders,
                               active_tables=active_tables,
                               total_tables=total_tables,
                               low_stock_count=low_stock_count,
                               recent_orders=recent_orders,
                               tables=tables,
                               audit_logs=audit_logs)

    @app.route('/tables')
    def tables():
        conn = get_db_connection()
        cur = conn.cursor()
        tables_list = cur.execute("SELECT * FROM dining_tables ORDER BY table_number").fetchall()
        reservations = cur.execute("""
            SELECT r.*, c.name AS customer_name, c.phone AS customer_phone, t.table_number
            FROM reservations r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN dining_tables t ON r.table_id = t.table_id
            ORDER BY r.reservation_time ASC
        """).fetchall()
        customers = cur.execute("SELECT * FROM customers ORDER BY name").fetchall()
        conn.close()
        return render_template('tables.html', tables=tables_list, reservations=reservations, customers=customers)

    @app.route('/tables/reserve', methods=['POST'])
    def reserve_table():
        customer_id = request.form.get('customer_id')
        table_id = request.form.get('table_id')
        res_time = request.form.get('reservation_time')
        guests = request.form.get('guest_count')
        requests = request.form.get('special_requests', '')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (customer_id, table_id, reservation_time, guest_count, special_requests, status)
            VALUES (?, ?, ?, ?, ?, 'Confirmed')
        """, (customer_id, table_id, res_time, guests, requests))
        cur.execute("UPDATE dining_tables SET status = 'Reserved' WHERE table_id = ?", (table_id,))
        cur.execute("""
            INSERT INTO audit_logs (entity_name, operation, record_id, message)
            VALUES ('reservations', 'INSERT', (SELECT last_insert_rowid()), 'Table reserved for guest size ' || ?)
        """, (guests,))
        conn.commit()
        conn.close()
        flash('Reservation confirmed successfully!', 'success')
        return redirect(url_for('tables'))

    @app.route('/menu')
    def menu():
        conn = get_db_connection()
        cur = conn.cursor()
        categories = cur.execute("SELECT * FROM categories ORDER BY display_order").fetchall()
        items = cur.execute("""
            SELECT m.*, c.category_name 
            FROM menu_items m
            JOIN categories c ON m.category_id = c.category_id
            ORDER BY c.display_order, m.name
        """).fetchall()
        conn.close()
        return render_template('menu.html', categories=categories, items=items)

    @app.route('/menu/update-price', methods=['POST'])
    def update_menu_price():
        item_id = request.form.get('item_id')
        new_price = request.form.get('new_price')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE menu_items SET price = ? WHERE item_id = ?", (new_price, item_id))
        conn.commit()
        conn.close()
        flash(f'Item price updated to ₹{new_price}. Trigger trg_menu_price_audit logged this update.', 'info')
        return redirect(url_for('menu'))

    @app.route('/pos')
    def pos():
        conn = get_db_connection()
        cur = conn.cursor()
        tables = cur.execute("SELECT * FROM dining_tables WHERE status != 'Maintenance' ORDER BY table_number").fetchall()
        customers = cur.execute("SELECT * FROM customers ORDER BY name").fetchall()
        waiters = cur.execute("SELECT user_id, full_name FROM users WHERE role = 'Waiter'").fetchall()
        categories = cur.execute("SELECT * FROM categories ORDER BY display_order").fetchall()
        items = cur.execute("SELECT * FROM menu_items WHERE is_available = 1 ORDER BY name").fetchall()
        
        # Active orders awaiting settlement
        active_orders = cur.execute("""
            SELECT o.*, t.table_number, c.name AS customer_name
            FROM orders o
            LEFT JOIN dining_tables t ON o.table_id = t.table_id
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_status NOT IN ('Completed', 'Cancelled')
            ORDER BY o.created_at DESC
        """).fetchall()

        conn.close()
        return render_template('pos.html',
                               tables=tables,
                               customers=customers,
                               waiters=waiters,
                               categories=categories,
                               items=items,
                               active_orders=active_orders)

    @app.route('/pos/create-order', methods=['POST'])
    def create_order():
        data = request.get_json() if request.is_json else request.form
        table_id = data.get('table_id') or None
        customer_id = data.get('customer_id') or None
        waiter_id = data.get('waiter_id') or None
        order_type = data.get('order_type', 'Dine-In')
        items = data.get('items', [])
        
        if isinstance(items, str):
            items = json.loads(items)

        if not items:
            return jsonify({'success': False, 'error': 'No items selected for order.'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate unique order number
        order_num = f"ORD-{int(datetime.now().timestamp())}"
        
        cur.execute("""
            INSERT INTO orders (order_number, table_id, customer_id, waiter_id, order_type, order_status)
            VALUES (?, ?, ?, ?, ?, 'In-Kitchen')
        """, (order_num, table_id, customer_id, waiter_id, order_type))
        order_id = cur.lastrowid

        # Insert items (triggers will recalculate subtotal, tax, grand_total, and update table status)
        for item in items:
            item_id = item['item_id']
            qty = int(item['quantity'])
            cur.execute("SELECT price FROM menu_items WHERE item_id = ?", (item_id,))
            price = cur.fetchone()[0]
            line_total = price * qty
            cur.execute("""
                INSERT INTO order_items (order_id, item_id, quantity, unit_price, line_total, kitchen_status)
                VALUES (?, ?, ?, ?, ?, 'Queued')
            """, (order_id, item_id, qty, price, line_total))

        conn.commit()
        conn.close()

        if request.is_json:
            return jsonify({'success': True, 'order_id': order_id, 'order_number': order_num})
        flash(f'Order {order_num} created! Trigger updated table and subtotal.', 'success')
        return redirect(url_for('pos'))

    @app.route('/kitchen')
    def kitchen():
        conn = get_db_connection()
        cur = conn.cursor()
        tickets = cur.execute("""
            SELECT oi.order_item_id, oi.order_id, oi.quantity, oi.kitchen_status, oi.customization_notes,
                   m.name AS item_name, m.dietary_type, m.preparation_time_mins,
                   o.order_number, o.order_type, t.table_number, oi.added_at
            FROM order_items oi
            JOIN menu_items m ON oi.item_id = m.item_id
            JOIN orders o ON oi.order_id = o.order_id
            LEFT JOIN dining_tables t ON o.table_id = t.table_id
            WHERE oi.kitchen_status IN ('Queued', 'Cooking', 'Ready')
            ORDER BY oi.added_at ASC
        """).fetchall()
        conn.close()
        return render_template('kitchen.html', tickets=tickets)

    @app.route('/kitchen/update-status', methods=['POST'])
    def update_kitchen_status():
        item_id = request.form.get('order_item_id')
        new_status = request.form.get('status')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE order_items SET kitchen_status = ? WHERE order_item_id = ?", (new_status, item_id))
        conn.commit()
        conn.close()
        flash(f'Kitchen ticket updated to {new_status}.', 'info')
        return redirect(url_for('kitchen'))

    @app.route('/inventory')
    def inventory():
        conn = get_db_connection()
        cur = conn.cursor()
        inventory_items = cur.execute("SELECT * FROM inventory_items ORDER BY name").fetchall()
        recipes = cur.execute("""
            SELECT mr.recipe_id, m.name AS menu_item, ii.name AS ingredient_name, mr.quantity_required, ii.unit
            FROM menu_recipes mr
            JOIN menu_items m ON mr.item_id = m.item_id
            JOIN inventory_items ii ON mr.ingredient_id = ii.ingredient_id
            ORDER BY m.name
        """).fetchall()
        low_stock = cur.execute("SELECT * FROM v_low_stock_alerts").fetchall()
        conn.close()
        return render_template('inventory.html', inventory_items=inventory_items, recipes=recipes, low_stock=low_stock)

    @app.route('/inventory/restock', methods=['POST'])
    def restock():
        ingredient_id = request.form.get('ingredient_id')
        qty = float(request.form.get('quantity', 0))
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE inventory_items SET stock_quantity = stock_quantity + ?, last_restocked = CURRENT_TIMESTAMP WHERE ingredient_id = ?", (qty, ingredient_id))
        cur.execute("""
            INSERT INTO audit_logs (entity_name, operation, record_id, message)
            VALUES ('inventory_items', 'UPDATE', ?, 'Restocked ' || ? || ' units of inventory.')
        """, (ingredient_id, qty))
        conn.commit()
        conn.close()
        flash('Inventory restocked successfully!', 'success')
        return redirect(url_for('inventory'))

    @app.route('/dbms')
    def dbms():
        conn = get_db_connection()
        cur = conn.cursor()

        # Database Objects metadata
        tables_meta = []
        raw_tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name").fetchall()
        for t in raw_tables:
            tname = t['name']
            cols = cur.execute(f"PRAGMA table_info({tname})").fetchall()
            fks = cur.execute(f"PRAGMA foreign_key_list({tname})").fetchall()
            count = cur.execute(f"SELECT COUNT(*) FROM {tname}").fetchone()[0]
            tables_meta.append({'name': tname, 'columns': cols, 'fks': fks, 'count': count})

        # Views
        views_meta = []
        raw_views = cur.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name").fetchall()
        for v in raw_views:
            vname = v['name']
            sample = cur.execute(f"SELECT * FROM {vname} LIMIT 5").fetchall()
            cols = [desc[0] for desc in cur.description] if cur.description else []
            views_meta.append({'name': vname, 'columns': cols, 'sample': sample})

        # Triggers
        triggers_meta = cur.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='trigger' ORDER BY tbl_name").fetchall()

        # Audit Logs
        audit_logs = cur.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 20").fetchall()

        # Active orders eligible for ACID simulation
        active_orders = cur.execute("SELECT order_id, order_number, grand_total, order_status FROM orders WHERE order_status NOT IN ('Completed', 'Cancelled')").fetchall()

        conn.close()
        return render_template('dbms_concepts.html',
                               tables_meta=tables_meta,
                               views_meta=views_meta,
                               triggers_meta=triggers_meta,
                               audit_logs=audit_logs,
                               active_orders=active_orders)

    @app.route('/api/acid-test', methods=['POST'])
    def api_acid_test():
        data = request.get_json() or {}
        order_id = data.get('order_id')
        payment_method = data.get('payment_method', 'UPI')
        fail_simulation = bool(data.get('fail_simulation', False))

        if not order_id:
            return jsonify({'success': False, 'error': 'Order ID is required.'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT grand_total FROM orders WHERE order_id = ?", (order_id,))
        order = cur.fetchone()
        conn.close()

        if not order:
            return jsonify({'success': False, 'error': 'Order not found.'}), 404

        result = execute_acid_transaction(order_id, payment_method, order['grand_total'], fail_simulation=fail_simulation)
        return jsonify(result)

    @app.route('/api/execute-sql', methods=['POST'])
    def api_execute_sql():
        data = request.get_json() or {}
        sql = data.get('sql', '').strip()

        if not sql:
            return jsonify({'success': False, 'error': 'Empty query.'}), 400

        # Safety restriction for academic query console: only SELECT and EXPLAIN
        sql_upper = sql.upper()
        if not (sql_upper.startswith('SELECT') or sql_upper.startswith('EXPLAIN')):
            return jsonify({'success': False, 'error': 'Interactive SQL Console is restricted to SELECT and EXPLAIN queries for safe evaluation.'}), 400

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(sql)
            rows = [dict(r) for r in cur.fetchall()]
            cols = [desc[0] for desc in cur.description] if cur.description else []
            conn.close()
            return jsonify({'success': True, 'columns': cols, 'rows': rows, 'count': len(rows)})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/reports')
    def reports():
        conn = get_db_connection()
        cur = conn.cursor()
        daily_sales = cur.execute("SELECT * FROM v_daily_sales_summary ORDER BY sale_date DESC").fetchall()
        top_items = cur.execute("SELECT * FROM v_top_selling_items ORDER BY total_quantity_sold DESC LIMIT 10").fetchall()
        staff_perf = cur.execute("SELECT * FROM v_staff_performance ORDER BY total_revenue_handled DESC").fetchall()
        conn.close()
        return render_template('reports.html', daily_sales=daily_sales, top_items=top_items, staff_perf=staff_perf)

    return app
