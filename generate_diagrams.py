import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('docs/images', exist_ok=True)

# -------------------------------------------------------------
# 1. ER DIAGRAM GENERATION
# -------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    ax.text(8, 10.6, "ENTITY-RELATIONSHIP (ER) DIAGRAM - DineFlow RMS", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1e1b4b')
    ax.text(8, 10.2, "Relational Entities, Attributes, Keys & Cardinality Mapping (B.Tech CSE Project - Gautam Soni)", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#475569')

    # Entity box definition helper
    def draw_entity(x, y, w, h, title, pk, fks, attrs, header_color='#3b82f6'):
        # Outer box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor='#ffffff', edgecolor='#64748b', linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        # Header box
        hdr = patches.FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor=header_color, edgecolor=header_color, linewidth=1, zorder=3)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.22, title, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=4)

        # Content
        cur_y = y + h - 0.65
        ax.text(x + 0.12, cur_y, f"🔑 {pk}", fontsize=7.5, fontweight='bold', color='#b91c1c', zorder=4)
        cur_y -= 0.22
        for fk in fks:
            ax.text(x + 0.12, cur_y, f"🔗 {fk}", fontsize=7.2, fontweight='bold', color='#4338ca', zorder=4)
            cur_y -= 0.20
        for a in attrs:
            ax.text(x + 0.12, cur_y, f"• {a}", fontsize=7, color='#334155', zorder=4)
            cur_y -= 0.18

    # Draw entities across grid
    # Row 1 (Top)
    draw_entity(0.5, 7.6, 2.7, 2.1, "USERS", "user_id", [], ["username", "full_name", "role", "email", "phone"], '#1e293b')
    draw_entity(4.0, 7.6, 2.7, 2.1, "DINING_TABLES", "table_id", [], ["table_number (U)", "capacity", "seating_section", "status"], '#0284c7')
    draw_entity(7.5, 7.6, 2.7, 2.1, "CUSTOMERS", "customer_id", [], ["name", "phone (U)", "email", "loyalty_points", "registered_at"], '#059669')
    draw_entity(11.0, 7.6, 2.8, 2.1, "RESERVATIONS", "reservation_id", ["customer_id", "table_id"], ["reservation_time", "guest_count", "status"], '#7c3aed')

    # Row 2 (Middle)
    draw_entity(0.5, 4.3, 2.7, 2.5, "ORDERS", "order_id", ["table_id", "customer_id", "waiter_id"], ["order_number (U)", "order_type", "order_status", "subtotal", "tax_amount", "grand_total"], '#ea580c')
    draw_entity(4.0, 4.3, 2.7, 2.5, "ORDER_ITEMS", "order_item_id", ["order_id", "item_id"], ["quantity", "unit_price", "line_total", "kitchen_status"], '#d97706')
    draw_entity(7.5, 4.3, 2.7, 2.5, "MENU_ITEMS", "item_id", ["category_id"], ["name (U)", "price", "dietary_type", "preparation_time", "is_available"], '#16a34a')
    draw_entity(11.0, 4.3, 2.8, 2.5, "CATEGORIES", "category_id", [], ["category_name (U)", "description", "display_order"], '#475569')

    # Row 3 (Bottom)
    draw_entity(0.5, 1.2, 2.7, 2.3, "PAYMENTS", "payment_id", ["order_id (U)"], ["payment_method", "amount_paid", "transaction_ref", "payment_status", "payment_time"], '#0d9488')
    draw_entity(4.0, 1.2, 2.7, 2.3, "MENU_RECIPES (BOM)", "recipe_id", ["item_id", "ingredient_id"], ["quantity_required", "UNIQUE(item, ingr)"], '#6366f1')
    draw_entity(7.5, 1.2, 2.7, 2.3, "INVENTORY_ITEMS", "ingredient_id", [], ["name (U)", "stock_quantity", "unit", "reorder_level", "supplier_name"], '#be123c')
    draw_entity(11.0, 1.2, 2.8, 2.3, "AUDIT_LOGS", "log_id", [], ["entity_name", "operation", "record_id", "message", "timestamp"], '#334155')

    # Relationship connectors
    def draw_rel(x1, y1, x2, y2, label1, label2, rel_name):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--"))
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my, rel_name, fontsize=6.8, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='#f1f5f9', edgecolor='#94a3b8', alpha=0.9))
        ax.text(x1, y1, label1, fontsize=7, fontweight='bold', color='#1e293b')
        ax.text(x2, y2, label2, fontsize=7, fontweight='bold', color='#1e293b')

    # Connections
    draw_rel(3.2, 5.5, 4.0, 5.5, "1", "M", "contains")
    draw_rel(6.7, 5.5, 7.5, 5.5, "M", "1", "references")
    draw_rel(10.2, 5.5, 11.0, 5.5, "M", "1", "belongs to")
    draw_rel(1.8, 4.3, 1.8, 3.5, "1", "1", "settled by")
    draw_rel(5.3, 4.3, 5.3, 3.5, "1", "M", "specifies")
    draw_rel(6.7, 2.3, 7.5, 2.3, "M", "1", "consumes")
    draw_rel(5.3, 7.6, 2.5, 6.8, "1", "M", "accommodates")
    draw_rel(8.8, 7.6, 2.8, 6.8, "1", "M", "places")
    draw_rel(8.8, 8.6, 11.0, 8.6, "1", "M", "books")

    plt.tight_layout()
    output_path = 'docs/images/er_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated ER Diagram: {output_path}")

# -------------------------------------------------------------
# 2. CLASS DIAGRAM GENERATION
# -------------------------------------------------------------
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Title
    ax.text(8, 10.6, "OBJECT CLASS DIAGRAM - DineFlow RMS", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1e1b4b')
    ax.text(8, 10.2, "Logical Domain Classes, Attributes, Operations & Encapsulation (B.Tech CSE Project - Gautam Soni)", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#475569')

    def draw_class(x, y, w, h, name, attrs, methods, color='#4338ca'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor='#ffffff', edgecolor='#475569', linewidth=1.4)
        ax.add_patch(rect)
        hdr = patches.FancyBboxPatch((x, y + h - 0.42), w, 0.42, boxstyle="round,pad=0.06,rounding_size=0.12",
                                     facecolor=color, edgecolor=color, linewidth=1)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.21, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white')

        cur_y = y + h - 0.60
        for a in attrs:
            ax.text(x + 0.12, cur_y, a, fontsize=6.8, color='#1e293b')
            cur_y -= 0.17
        
        ax.plot([x + 0.05, x + w - 0.05], [cur_y + 0.05, cur_y + 0.05], color='#cbd5e1', lw=1)
        cur_y -= 0.14
        
        for m in methods:
            ax.text(x + 0.12, cur_y, m, fontsize=6.8, color='#0369a1', fontstyle='italic')
            cur_y -= 0.17

    # Draw Classes
    draw_class(0.6, 7.3, 2.7, 2.5, "User", 
               ["- userId: int", "- username: str", "- passwordHash: str", "- fullName: str", "- role: UserRole"], 
               ["+ authenticate()", "+ changePassword()", "+ getAssignedOrders()"], '#1e293b')

    draw_class(4.1, 7.3, 2.7, 2.5, "DiningTable", 
               ["- tableId: int", "- tableNumber: str", "- capacity: int", "- section: str", "- status: TableStatus"], 
               ["+ markOccupied()", "+ markAvailable()", "+ reserveTable()"], '#0284c7')

    draw_class(7.6, 7.3, 2.7, 2.5, "Customer", 
               ["- customerId: int", "- name: str", "- phone: str", "- email: str", "- loyaltyPoints: int"], 
               ["+ addLoyaltyPoints()", "+ redeemPoints()", "+ getOrderHistory()"], '#059669')

    draw_class(11.1, 7.3, 2.7, 2.5, "Reservation", 
               ["- reservationId: int", "- customerId: int", "- tableId: int", "- reservationTime: datetime", "- guestCount: int"], 
               ["+ confirmBooking()", "+ cancelBooking()", "+ seatGuests()"], '#7c3aed')

    draw_class(0.6, 4.0, 2.7, 2.8, "Order", 
               ["- orderId: int", "- orderNumber: str", "- tableId: int", "- orderType: str", "- orderStatus: str", "- grandTotal: float"], 
               ["+ addItem(item, qty)", "+ removeItem(orderItemId)", "+ calculateTotals()", "+ completeOrder()"], '#ea580c')

    draw_class(4.1, 4.0, 2.7, 2.8, "OrderItem", 
               ["- orderItemId: int", "- orderId: int", "- itemId: int", "- quantity: int", "- unitPrice: float", "- lineTotal: float"], 
               ["+ updateQuantity()", "+ updateStatus()", "+ getLineSubtotal()"], '#d97706')

    draw_class(7.6, 4.0, 2.7, 2.8, "MenuItem", 
               ["- itemId: int", "- categoryId: int", "- name: str", "- price: float", "- dietaryType: str", "- isAvailable: bool"], 
               ["+ updatePrice()", "+ toggleAvailability()", "+ getRecipeBOM()"], '#16a34a')

    draw_class(11.1, 4.0, 2.7, 2.8, "Category", 
               ["- categoryId: int", "- categoryName: str", "- description: str", "- displayOrder: int"], 
               ["+ getMenuItems()", "+ updateCategory()"], '#475569')

    draw_class(0.6, 1.0, 2.7, 2.5, "Payment", 
               ["- paymentId: int", "- orderId: int", "- paymentMethod: str", "- amountPaid: float", "- txnRef: str"], 
               ["+ processPayment()", "+ generateInvoice()", "+ verifySuccess()"], '#0d9488')

    draw_class(4.1, 1.0, 2.7, 2.5, "InventoryItem", 
               ["- ingredientId: int", "- name: str", "- stockQuantity: float", "- unit: str", "- reorderLevel: float"], 
               ["+ deductStock(amount)", "+ restock(amount)", "+ checkLowStock()"], '#be123c')

    draw_class(7.6, 1.0, 2.7, 2.5, "MenuRecipe", 
               ["- recipeId: int", "- itemId: int", "- ingredientId: int", "- quantityRequired: float"], 
               ["+ calculateDeduction()", "+ updateRecipe()"], '#6366f1')

    draw_class(11.1, 1.0, 2.7, 2.5, "TransactionManager", 
               ["- connection: DBConnection", "- isolationLevel: str"], 
               ["+ beginTransaction()", "+ commitCheckout()", "+ rollbackTransaction()", "+ logAuditTrail()"], '#b45309')

    # Association Lines
    ax.annotate('', xy=(3.3, 5.4), xytext=(4.1, 5.4), arrowprops=dict(arrowstyle="<|-", color="#475569", lw=1.2))
    ax.annotate('', xy=(6.8, 5.4), xytext=(7.6, 5.4), arrowprops=dict(arrowstyle="<|-", color="#475569", lw=1.2))
    ax.annotate('', xy=(10.3, 5.4), xytext=(11.1, 5.4), arrowprops=dict(arrowstyle="<|-", color="#475569", lw=1.2))
    ax.annotate('', xy=(1.95, 3.5), xytext=(1.95, 4.0), arrowprops=dict(arrowstyle="<|-", color="#475569", lw=1.2))

    plt.tight_layout()
    output_path = 'docs/images/class_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated Class Diagram: {output_path}")

generate_er_diagram()
generate_class_diagram()
