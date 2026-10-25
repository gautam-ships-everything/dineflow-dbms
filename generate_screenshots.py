import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('docs/images', exist_ok=True)

def generate_dashboard_mockup():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=250)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Background
    ax.add_patch(patches.Rectangle((0, 0), 12, 7.5, facecolor='#f8fafc'))

    # Top Academic banner
    ax.add_patch(patches.Rectangle((0, 7.1), 12, 0.4, facecolor='#1e1b4b'))
    ax.text(0.3, 7.3, "IPS ACADEMY INDORE | CSE DEPARTMENT (2026-27)", color='white', fontsize=7.5, fontweight='bold', va='center')
    ax.text(11.7, 7.3, "DineFlow DBMS | Gautam Soni (0808CS241120)", color='#fde047', fontsize=7.5, fontweight='bold', ha='right', va='center')

    # Navbar
    ax.add_patch(patches.Rectangle((0, 6.4), 12, 0.7, facecolor='white', edgecolor='#e2e8f0'))
    ax.text(0.4, 6.75, "DineFlow", color='#ea580c', fontsize=12, fontweight='bold', va='center')
    ax.text(2.2, 6.75, "Dashboard   |   Tables & Seating   |   Menu   |   POS & Billing   |   Kitchen KOT   |   Inventory   |   DBMS Concepts Lab", 
            color='#475569', fontsize=8, va='center')

    # Page Header
    ax.text(0.5, 5.95, "Executive Operations Dashboard", fontsize=13, fontweight='bold', color='#0f172a')
    ax.text(0.5, 5.7, "Real-time overview of restaurant tables, kitchen queue, inventory, and database metrics.", fontsize=8, color='#64748b')

    # 4 KPI Cards
    def draw_kpi(x, label, val, sub, bg, border, tc):
        ax.add_patch(patches.FancyBboxPatch((x, 4.4), 2.5, 0.95, boxstyle="round,pad=0.05,rounding_size=0.1",
                                            facecolor=bg, edgecolor=border, lw=1))
        ax.text(x + 0.2, 5.05, label, fontsize=7.5, color='#64748b', fontweight='bold')
        ax.text(x + 0.2, 4.7, val, fontsize=12, color=tc, fontweight='bold')
        ax.text(x + 0.2, 4.5, sub, fontsize=6.8, color='#94a3b8')

    draw_kpi(0.5, "TOTAL REVENUE", "Rs. 2,664.25", "2 orders completed", '#ffffff', '#e2e8f0', '#0f172a')
    draw_kpi(3.3, "TOTAL ORDERS", "3 Placed", "1 active in-kitchen", '#ffffff', '#e2e8f0', '#0284c7')
    draw_kpi(6.1, "TABLE OCCUPANCY", "1 / 12 Active", "2 reserved, 9 available", '#ffffff', '#e2e8f0', '#16a34a')
    draw_kpi(8.9, "LOW STOCK ALERTS", "1 Deficit Item", "Saffron & Spices below min", '#fff1f2', '#fecdd3', '#dc2626')

    # Left Card: Live Floor Plan
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.6), 5.3, 3.5, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#e2e8f0', lw=1))
    ax.text(0.7, 3.8, "Live Floor Plan (Auto-Synced via Triggers)", fontsize=9.5, fontweight='bold', color='#0f172a')

    # Draw table boxes
    tables_data = [
        ("T-01", "Available", '#f0fdf4', '#10b981', '#065f46'),
        ("T-02", "Occupied", '#fef2f2', '#ef4444', '#991b1b'),
        ("T-03", "Available", '#f0fdf4', '#10b981', '#065f46'),
        ("AC-01", "Available", '#f0fdf4', '#10b981', '#065f46'),
        ("AC-02", "Available", '#f0fdf4', '#10b981', '#065f46'),
        ("RT-01", "Reserved", '#fffbeb', '#f59e0b', '#92400e')
    ]
    for idx, (tnum, st, bg, bc, tc) in enumerate(tables_data):
        col = idx % 3
        row = idx // 3
        tx = 0.8 + col * 1.6
        ty = 2.4 - row * 1.2
        ax.add_patch(patches.FancyBboxPatch((tx, ty), 1.4, 0.95, boxstyle="round,pad=0.04,rounding_size=0.08",
                                            facecolor=bg, edgecolor=bc, lw=1.2))
        ax.text(tx + 0.7, ty + 0.6, tnum, ha='center', fontsize=9.5, fontweight='bold', color='#1e293b')
        ax.text(tx + 0.7, ty + 0.25, st, ha='center', fontsize=7.2, fontweight='bold', color=tc)

    # Right Card: Recent Trigger Activity
    ax.add_patch(patches.FancyBboxPatch((6.1, 0.6), 5.4, 3.5, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#e2e8f0', lw=1))
    ax.text(6.3, 3.8, "Active DBMS Trigger Audit Log", fontsize=9.5, fontweight='bold', color='#0f172a')

    logs = [
        ("order_items", "INSERT", "Item added to order #3. Recalculated subtotal & tax.", "15:22:10"),
        ("dining_tables", "UPDATE", "Table #2 marked Occupied due to new Order ORD-1003", "15:22:10"),
        ("payments", "INSERT", "Payment completed for Order #2. Table released.", "14:10:05"),
        ("menu_items", "UPDATE", "Price updated for Paneer Butter Masala (Rs. 320 -> 340)", "13:05:40")
    ]
    cur_y = 3.3
    for ent, op, msg, tm in logs:
        ax.text(6.3, cur_y, f"[{ent}] {op}: {msg[:42]}...", fontsize=7.2, color='#334155')
        ax.text(11.3, cur_y, tm, fontsize=6.8, color='#94a3b8', ha='right')
        cur_y -= 0.6

    plt.tight_layout()
    plt.savefig('docs/images/dashboard_screenshot.png', dpi=250, bbox_inches='tight')
    plt.close()
    print("Generated docs/images/dashboard_screenshot.png")

def generate_pos_mockup():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=250)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 12, 7.5, facecolor='#f8fafc'))
    # Banner & Navbar
    ax.add_patch(patches.Rectangle((0, 7.1), 12, 0.4, facecolor='#1e1b4b'))
    ax.text(0.3, 7.3, "IPS ACADEMY INDORE | CSE DEPARTMENT (2026-27)", color='white', fontsize=7.5, fontweight='bold', va='center')
    ax.text(11.7, 7.3, "DineFlow DBMS | Gautam Soni (0808CS241120)", color='#fde047', fontsize=7.5, fontweight='bold', ha='right', va='center')

    ax.add_patch(patches.Rectangle((0, 6.4), 12, 0.7, facecolor='white', edgecolor='#e2e8f0'))
    ax.text(0.4, 6.75, "DineFlow POS & Billing", color='#ea580c', fontsize=12, fontweight='bold', va='center')

    # Left: Menu selection
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.6), 5.7, 5.5, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#e2e8f0', lw=1))
    ax.text(0.8, 5.75, "Menu Catalog Selection", fontsize=10.5, fontweight='bold', color='#0f172a')

    dishes = [
        ("Paneer Tikka Sunhari", "Veg", "Rs. 280.00"),
        ("Murgh Malai Tikka", "Non-Veg", "Rs. 340.00"),
        ("Paneer Butter Masala", "Veg", "Rs. 320.00"),
        ("Dal Makhani Heritage", "Veg", "Rs. 260.00"),
        ("Butter Chicken Delhi Style", "Non-Veg", "Rs. 390.00"),
        ("Garlic Butter Naan", "Veg", "Rs. 75.00"),
        ("Dum Biryani Lucknowi", "Non-Veg", "Rs. 360.00")
    ]
    dy = 5.2
    for name, tag, pr in dishes:
        ax.add_patch(patches.Rectangle((0.8, dy - 0.42), 5.1, 0.5, facecolor='#f8fafc', edgecolor='#e2e8f0', lw=0.8))
        ax.text(0.9, dy - 0.15, name, fontsize=8, fontweight='bold', color='#1e293b')
        ax.text(3.4, dy - 0.15, f"[{tag}]", fontsize=7, color='#16a34a' if tag=='Veg' else '#dc2626')
        ax.text(4.4, dy - 0.15, pr, fontsize=8, fontweight='bold', color='#ea580c')
        ax.text(5.5, dy - 0.15, "[+ Add]", fontsize=7.5, fontweight='bold', color='#0284c7')
        dy -= 0.65

    # Right: Order Cart & Summary
    ax.add_patch(patches.FancyBboxPatch((6.5, 0.6), 5.0, 5.5, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#e2e8f0', lw=1))
    ax.text(6.8, 5.75, "Live Order Bill & Trigger Calculation", fontsize=10.5, fontweight='bold', color='#0f172a')

    # Selected Items
    ax.text(6.8, 5.3, "Table: T-02 (AC Dining)  |  Customer: Rohan Singhal", fontsize=7.8, color='#475569')
    ax.text(6.8, 4.7, "• Paneer Tikka Sunhari (1x) .................... Rs. 280.00", fontsize=8, color='#334155')
    ax.text(6.8, 4.3, "• Dal Makhani Heritage (1x) ..................... Rs. 260.00", fontsize=8, color='#334155')
    ax.text(6.8, 3.9, "• Veg Dum Biryani (1x) ........................... Rs. 280.00", fontsize=8, color='#334155')
    ax.text(6.8, 3.5, "• Blue Lagoon Mocktail (2x) .................... Rs. 300.00", fontsize=8, color='#334155')

    # Bill Summary
    ax.add_patch(patches.Rectangle((6.8, 1.8), 4.4, 1.4, facecolor='#f8fafc', edgecolor='#cbd5e1'))
    ax.text(7.0, 2.9, "Subtotal: Rs. 1,120.00", fontsize=8.5, color='#334155')
    ax.text(7.0, 2.55, "GST (5% Trigger Calculated): Rs. 56.00", fontsize=8.5, color='#0284c7')
    ax.text(7.0, 2.1, "Grand Total: Rs. 1,176.00", fontsize=11, fontweight='bold', color='#ea580c')

    # Place order button
    ax.add_patch(patches.FancyBboxPatch((6.8, 1.0), 4.4, 0.55, boxstyle="round,pad=0.04,rounding_size=0.08",
                                        facecolor='#ea580c', edgecolor='#ea580c'))
    ax.text(9.0, 1.25, "Place Order (Triggers Fired: Tax & Table Status)", color='white', ha='center', va='center', fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig('docs/images/pos_screenshot.png', dpi=250, bbox_inches='tight')
    plt.close()
    print("Generated docs/images/pos_screenshot.png")

def generate_dbms_console_mockup():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=250)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, 0), 12, 7.5, facecolor='#f8fafc'))
    # Banner & Navbar
    ax.add_patch(patches.Rectangle((0, 7.1), 12, 0.4, facecolor='#1e1b4b'))
    ax.text(0.3, 7.3, "IPS ACADEMY INDORE | CSE DEPARTMENT (2026-27)", color='white', fontsize=7.5, fontweight='bold', va='center')
    ax.text(11.7, 7.3, "DineFlow DBMS | Gautam Soni (0808CS241120)", color='#fde047', fontsize=7.5, fontweight='bold', ha='right', va='center')

    ax.add_patch(patches.Rectangle((0, 6.4), 12, 0.7, facecolor='white', edgecolor='#e2e8f0'))
    ax.text(0.4, 6.75, "DBMS Concepts Demonstration Lab", color='#4f46e5', fontsize=12, fontweight='bold', va='center')

    # Top: ACID Simulator Box
    ax.add_patch(patches.FancyBboxPatch((0.5, 3.8), 11.0, 2.3, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#cbd5e1', lw=1.2))
    ax.text(0.8, 5.75, "ACID Transaction Simulator: Atomic Multi-Table Checkout", fontsize=10.5, fontweight='bold', color='#1e1b4b')
    ax.text(0.8, 5.4, "Order: ORD-1003 (Rs. 1,176.00)  |  Payment: UPI  |  Triggers: Table Free + Inventory BOM Deduction", fontsize=8, color='#475569')

    # Commit step trace
    ax.text(0.8, 4.95, "[OK] STEP 1: BEGIN TRANSACTION started.", fontsize=7.5, color='#16a34a', fontfamily='monospace')
    ax.text(0.8, 4.70, "[OK] STEP 2: Order #3 verified; payment record inserted into payments table.", fontsize=7.5, color='#16a34a', fontfamily='monospace')
    ax.text(0.8, 4.45, "[OK] STEP 3: Deducted ingredients from inventory_items via menu_recipes BOM.", fontsize=7.5, color='#16a34a', fontfamily='monospace')
    ax.text(0.8, 4.20, "[OK] STEP 4: Table status auto-freed to 'Available' and loyalty points credited.", fontsize=7.5, color='#16a34a', fontfamily='monospace')
    ax.text(0.8, 3.95, "[OK] STEP 5: COMMIT SUCCESSFUL. Durably written to database file.", fontsize=7.8, color='#16a34a', fontweight='bold', fontfamily='monospace')

    # Bottom: Interactive SQL Console
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.6), 11.0, 2.9, boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor='white', edgecolor='#cbd5e1', lw=1.2))
    ax.text(0.8, 3.15, "Interactive SQL Query Runner & Query Optimizer (EXPLAIN QUERY PLAN)", fontsize=10, fontweight='bold', color='#0f172a')

    # Terminal box
    ax.add_patch(patches.Rectangle((0.8, 1.8), 10.4, 1.0, facecolor='#0f172a', edgecolor='#334155'))
    ax.text(0.95, 2.5, "EXPLAIN QUERY PLAN", fontsize=8, color='#38bdf8', fontfamily='monospace', fontweight='bold')
    ax.text(0.95, 2.2, "SELECT o.order_number, c.name, o.grand_total FROM orders o JOIN customers c ON o.customer_id = c.customer_id;", 
            fontsize=7.5, color='#a5f3fc', fontfamily='monospace')
    ax.text(0.95, 1.95, "-- SCAN orders (idx_orders_customer) & SEARCH TABLE customers USING INTEGER PRIMARY KEY (rowid=?)", 
            fontsize=7.2, color='#34d399', fontfamily='monospace')

    # Result summary
    ax.text(0.8, 1.35, "Result: Query executed in 1.4ms using B-Tree index idx_orders_customer.", fontsize=8, color='#0284c7', fontweight='bold')
    ax.text(0.8, 1.0, "Database Views Available: v_daily_sales_summary, v_top_selling_items, v_table_occupancy_status, v_low_stock_alerts", fontsize=7.5, color='#64748b')

    plt.tight_layout()
    plt.savefig('docs/images/dbms_console_screenshot.png', dpi=250, bbox_inches='tight')
    plt.close()
    print("Generated docs/images/dbms_console_screenshot.png")

generate_dashboard_mockup()
generate_pos_mockup()
generate_dbms_console_mockup()
