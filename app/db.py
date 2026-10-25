import os
import sqlite3
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database')
DB_PATH = os.path.join(DB_DIR, 'restaurant.db')

def get_db_connection():
    """Returns a SQLite connection with row_factory set and foreign keys enabled."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(force_recreate=False):
    """Initializes schema and seeds realistic data."""
    if force_recreate and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    if not os.path.exists(DB_PATH) or force_recreate:
        os.makedirs(DB_DIR, exist_ok=True)
        conn = get_db_connection()
        cur = conn.cursor()

        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_file, 'r', encoding='utf-8') as f:
            cur.executescript(f.read())

        seed_file = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
        with open(seed_file, 'r', encoding='utf-8') as f:
            cur.executescript(f.read())

        conn.commit()
        conn.close()
        print(f"Database successfully initialized at {DB_PATH}")

def execute_query(query, params=(), fetch_mode='all'):
    """Executes a query safely with parameter binding."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    
    if fetch_mode == 'all':
        res = [dict(row) for row in cur.fetchall()]
    elif fetch_mode == 'one':
        row = cur.fetchone()
        res = dict(row) if row else None
    elif fetch_mode == 'commit':
        conn.commit()
        res = cur.lastrowid
    else:
        res = None
        
    conn.close()
    return res

def execute_acid_transaction(order_id, payment_method, amount, fail_simulation=False):
    """
    Demonstrates ACID Properties:
    A (Atomicity): All steps succeed or all rollback.
    C (Consistency): Constraints and foreign keys are preserved.
    I (Isolation): Managed by SQLite transaction locks.
    D (Durability): Written to permanent database file upon commit.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    steps_log = []
    
    try:
        cur.execute("BEGIN TRANSACTION;")
        steps_log.append("STEP 1: BEGIN TRANSACTION started.")
        
        # Verify order exists and is valid
        cur.execute("SELECT order_id, table_id, grand_total, order_status FROM orders WHERE order_id = ?", (order_id,))
        order = cur.fetchone()
        if not order:
            raise ValueError(f"Order #{order_id} does not exist.")
        
        steps_log.append(f"STEP 2: Verified Order #{order_id} (Status: {order['order_status']}, Total: ₹{order['grand_total']}).")

        # Step 3: Insert payment
        txn_ref = f"TXN-ACID-{int(datetime.now().timestamp())}"
        cur.execute("""
            INSERT INTO payments (order_id, payment_method, amount_paid, transaction_reference, payment_status)
            VALUES (?, ?, ?, ?, 'Success')
        """, (order_id, payment_method, amount, txn_ref))
        steps_log.append(f"STEP 3: Payment of ₹{amount} recorded with reference {txn_ref}.")

        # Step 4: Deduct Inventory items using Bill of Materials (menu_recipes)
        cur.execute("""
            SELECT mr.ingredient_id, ii.name AS ingredient_name, (mr.quantity_required * oi.quantity) AS deduction_qty, ii.stock_quantity
            FROM order_items oi
            JOIN menu_recipes mr ON oi.item_id = mr.item_id
            JOIN inventory_items ii ON mr.ingredient_id = ii.ingredient_id
            WHERE oi.order_id = ?
        """, (order_id,))
        deductions = cur.fetchall()

        for d in deductions:
            if fail_simulation:
                # Deliberate failure trigger to demonstrate ACID Rollback
                raise RuntimeError(f"SIMULATED ACID FAILURE: Payment Gateway timeout or Inventory stock verification failure for '{d['ingredient_name']}'!")
            
            cur.execute("""
                UPDATE inventory_items
                SET stock_quantity = stock_quantity - ?
                WHERE ingredient_id = ?
            """, (d['deduction_qty'], d['ingredient_id']))
            steps_log.append(f"STEP 4: Deducted {d['deduction_qty']} {d['ingredient_name']} from Inventory.")

        # Note: Triggers automatically update order status to 'Completed' and table status to 'Available'
        conn.commit()
        steps_log.append("STEP 5: COMMIT SUCCESSFUL. All changes persisted durably.")
        return {"success": True, "steps": steps_log, "message": "Transaction committed successfully!"}

    except Exception as e:
        conn.rollback()
        steps_log.append(f"EXCEPTION OCCURRED: {str(e)}")
        steps_log.append("ROLLBACK EXECUTED: All changes discarded. Database remains in consistent pre-transaction state.")
        return {"success": False, "steps": steps_log, "error": str(e)}
    finally:
        conn.close()
