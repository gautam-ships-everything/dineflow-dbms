// DineFlow - Client Side Logic & DBMS Live Lab Scripts
// Gautam Soni (0808CS241120)

// -------------------------------------------------------------
// POS Cart State
// -------------------------------------------------------------
let currentCart = [];

function addToCart(itemId, name, price) {
    const existing = currentCart.find(i => i.item_id === itemId);
    if (existing) {
        existing.quantity += 1;
    } else {
        currentCart.push({ item_id: itemId, name: name, price: price, quantity: 1 });
    }
    renderCart();
}

function updateCartQty(itemId, delta) {
    const item = currentCart.find(i => i.item_id === itemId);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity <= 0) {
        currentCart = currentCart.filter(i => i.item_id !== itemId);
    }
    renderCart();
}

function renderCart() {
    const container = document.getElementById('cart-items-container');
    const subtotalEl = document.getElementById('cart-subtotal');
    const taxEl = document.getElementById('cart-tax');
    const totalEl = document.getElementById('cart-total');
    const submitBtn = document.getElementById('submit-order-btn');

    if (!container) return;

    if (currentCart.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 30px; color:#94a3b8;">Cart is empty. Select menu items to create an order.</div>';
        if (subtotalEl) subtotalEl.innerText = '₹0.00';
        if (taxEl) taxEl.innerText = '₹0.00';
        if (totalEl) totalEl.innerText = '₹0.00';
        if (submitBtn) submitBtn.disabled = true;
        return;
    }

    let html = '';
    let subtotal = 0;

    currentCart.forEach(item => {
        const lineTotal = item.price * item.quantity;
        subtotal += lineTotal;
        html += `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #f1f5f9;">
                <div>
                    <div style="font-weight:600; font-size:0.9rem;">${item.name}</div>
                    <div style="font-size:0.8rem; color:#64748b;">₹${item.price.toFixed(2)} × ${item.quantity} = ₹${lineTotal.toFixed(2)}</div>
                </div>
                <div style="display:flex; align-items:center; gap:6px;">
                    <button class="btn btn-secondary btn-sm" onclick="updateCartQty(${item.item_id}, -1)">-</button>
                    <span style="font-weight:700; width:18px; text-align:center;">${item.quantity}</span>
                    <button class="btn btn-secondary btn-sm" onclick="updateCartQty(${item.item_id}, 1)">+</button>
                </div>
            </div>
        `;
    });

    const tax = subtotal * 0.05; // 5% GST
    const grandTotal = subtotal + tax;

    container.innerHTML = html;
    if (subtotalEl) subtotalEl.innerText = `₹${subtotal.toFixed(2)}`;
    if (taxEl) taxEl.innerText = `₹${tax.toFixed(2)}`;
    if (totalEl) totalEl.innerText = `₹${grandTotal.toFixed(2)}`;
    if (submitBtn) submitBtn.disabled = false;
}

function submitPOSOrder() {
    const tableId = document.getElementById('pos-table-select').value;
    const customerId = document.getElementById('pos-customer-select').value;
    const waiterId = document.getElementById('pos-waiter-select').value;
    const orderType = document.getElementById('pos-type-select').value;

    if (currentCart.length === 0) {
        alert('Please add items to cart before placing order.');
        return;
    }

    const payload = {
        table_id: tableId,
        customer_id: customerId,
        waiter_id: waiterId,
        order_type: orderType,
        items: currentCart
    };

    fetch('/pos/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`Order #${data.order_number} created successfully!\n\nDBMS Concepts Demonstrated:\n- Foreign Keys validated\n- Triggers calculated subtotal & tax\n- Table status automatically marked Occupied`);
            window.location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(err => {
        alert('Order submission failed: ' + err);
    });
}

// -------------------------------------------------------------
// ACID Transaction Interactive Simulator
// -------------------------------------------------------------
function runAcidSimulation(failSim) {
    const orderSelect = document.getElementById('acid-order-select');
    const payMethodSelect = document.getElementById('acid-method-select');
    const resultBox = document.getElementById('acid-result-box');

    if (!orderSelect || !orderSelect.value) {
        alert('Please select an active order to run the ACID simulation.');
        return;
    }

    resultBox.style.display = 'block';
    resultBox.innerHTML = '<div style="color:#64748b;">Processing transaction across database engine...</div>';

    fetch('/api/acid-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            order_id: orderSelect.value,
            payment_method: payMethodSelect.value,
            fail_simulation: failSim
        })
    })
    .then(r => r.json())
    .then(data => {
        let outHtml = `<div style="font-weight:700; margin-bottom:8px; color:${data.success ? '#10b981' : '#ef4444'};">
            ${data.success ? '✔ TRANSACTION COMMITTED SUCCESSFULLY' : '✖ TRANSACTION ABORTED & ROLLED BACK'}
        </div>`;
        outHtml += '<ul style="list-style:none; padding:0; font-family:monospace; font-size:0.85rem; line-height:1.6;">';
        data.steps.forEach(step => {
            const isErr = step.includes('EXCEPTION') || step.includes('ROLLBACK');
            const isOk = step.includes('COMMIT') || step.includes('SUCCESS');
            const color = isErr ? '#ef4444' : (isOk ? '#10b981' : '#334155');
            outHtml += `<li style="color:${color}; margin-bottom:4px;">${step}</li>`;
        });
        outHtml += '</ul>';
        resultBox.innerHTML = outHtml;
    })
    .catch(err => {
        resultBox.innerHTML = `<div style="color:#ef4444;">Network error: ${err}</div>`;
    });
}

// -------------------------------------------------------------
// Interactive SQL Runner
// -------------------------------------------------------------
function runInteractiveSql() {
    const editor = document.getElementById('sql-query-editor');
    const resultContainer = document.getElementById('sql-results-container');
    const metaContainer = document.getElementById('sql-meta-container');

    if (!editor) return;
    const query = editor.value.trim();

    resultContainer.innerHTML = '<div style="padding:15px; color:#64748b;">Executing query on SQLite engine...</div>';

    fetch('/api/execute-sql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sql: query })
    })
    .then(r => r.json())
    .then(data => {
        if (!data.success) {
            metaContainer.innerHTML = `<span class="badge badge-danger">Execution Error</span>`;
            resultContainer.innerHTML = `<div style="padding:15px; color:#ef4444; font-family:monospace;">${data.error}</div>`;
            return;
        }

        metaContainer.innerHTML = `<span class="badge badge-success">Success</span> Returned ${data.count} rows.`;

        if (data.rows.length === 0) {
            resultContainer.innerHTML = '<div style="padding:15px; color:#64748b;">Query returned 0 rows.</div>';
            return;
        }

        let tableHtml = '<table class="data-table"><thead><tr>';
        data.columns.forEach(col => {
            tableHtml += `<th>${col}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';

        data.rows.forEach(row => {
            tableHtml += '<tr>';
            data.columns.forEach(col => {
                tableHtml += `<td>${row[col] !== null ? row[col] : '<i style="color:#94a3b8;">NULL</i>'}</td>`;
            });
            tableHtml += '</tr>';
        });

        tableHtml += '</tbody></table>';
        resultContainer.innerHTML = tableHtml;
    })
    .catch(err => {
        resultContainer.innerHTML = `<div style="padding:15px; color:#ef4444;">Error: ${err}</div>`;
    });
}

function loadSampleQuery(query) {
    const editor = document.getElementById('sql-query-editor');
    if (editor) {
        editor.value = query;
        runInteractiveSql();
    }
}

// -------------------------------------------------------------
// Tab Switching
// -------------------------------------------------------------
function switchDbmsTab(tabId) {
    document.querySelectorAll('.dbms-tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.dbms-tab-btn').forEach(el => el.classList.remove('active'));

    const target = document.getElementById(tabId);
    if (target) target.style.display = 'block';

    const btn = document.getElementById('btn-' + tabId);
    if (btn) btn.classList.add('active');
}
