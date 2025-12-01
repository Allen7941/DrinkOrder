/* 管理頁邏輯 */

// ========== 飲料店管理 ==========

async function loadShopsAdmin() {
    const container = document.getElementById('shops-list');
    if (!container) return;

    try {
        const result = await api.get('/api/shops');
        if (result.success) {
            if (result.data.length === 0) {
                container.innerHTML = '<p>尚無飲料店資料</p>';
                return;
            }

            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>店家名稱</th>
                            <th>電話</th>
                            <th>地址</th>
                            <th>狀態</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            result.data.forEach(shop => {
                html += `
                    <tr>
                        <td>${shop.shop_name}</td>
                        <td>${shop.phone || '-'}</td>
                        <td>${shop.address || '-'}</td>
                        <td>${shop.is_active ? '✅ 啟用' : '❌ 停用'}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="editShop('${shop.shop_id}')">編輯</button>
                            <a href="/admin/shops/${shop.shop_id}/import-menu" class="btn btn-primary">匯入菜單</a>
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('載入飲料店失敗:', error);
    }
}

async function createShop() {
    const name = document.getElementById('new-shop-name').value;
    const phone = document.getElementById('new-shop-phone').value;
    const address = document.getElementById('new-shop-address').value;

    if (!name) {
        showAlert('請輸入店家名稱', 'error');
        return;
    }

    try {
        const result = await api.post('/api/shops', {
            shop_name: name,
            phone: phone,
            address: address
        });

        if (result.success) {
            showAlert('飲料店新增成功！', 'success');
            loadShopsAdmin();
            // 清空表單
            document.getElementById('new-shop-name').value = '';
            document.getElementById('new-shop-phone').value = '';
            document.getElementById('new-shop-address').value = '';
        } else {
            showAlert(result.message || '新增失敗', 'error');
        }
    } catch (error) {
        console.error('新增飲料店失敗:', error);
        showAlert('系統錯誤', 'error');
    }
}

// ========== 團購活動管理 ==========

async function loadEvents() {
    const container = document.getElementById('events-list');
    if (!container) return;

    try {
        const result = await api.get('/api/events');
        if (result.success) {
            if (result.data.length === 0) {
                container.innerHTML = '<p>尚無團購活動</p>';
                return;
            }

            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>飲料店</th>
                            <th>發起人</th>
                            <th>截止時間</th>
                            <th>訂單數</th>
                            <th>總金額</th>
                            <th>狀態</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            result.data.forEach(event => {
                const statusClass = event.status === '進行中' ? 'alert-success' :
                    event.status === '已截止' ? 'alert-info' : 'alert-error';
                html += `
                    <tr>
                        <td>${event.shop_name}</td>
                        <td>${event.created_by || '-'}</td>
                        <td>${event.deadline ? formatDateTime(event.deadline) : '-'}</td>
                        <td>${event.total_orders}</td>
                        <td>${formatCurrency(event.total_amount || 0)}</td>
                        <td><span class="alert ${statusClass}" style="padding: 4px 10px; margin: 0;">${event.status}</span></td>
                        <td>
                            <a href="/admin/orders?event_id=${event.event_id}" class="btn btn-primary">查看訂單</a>
                            ${event.status === '進行中' ? `<button class="btn btn-secondary" onclick="closeEvent('${event.event_id}')">關閉</button>` : ''}
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('載入團購活動失敗:', error);
    }
}

async function createEvent() {
    const shopId = document.getElementById('event-shop').value;
    const deadline = document.getElementById('event-deadline').value;
    const createdBy = document.getElementById('event-creator').value;
    const minQuantity = document.getElementById('event-min-quantity').value;

    if (!shopId) {
        showAlert('請選擇飲料店', 'error');
        return;
    }

    try {
        const result = await api.post('/api/events', {
            shop_id: shopId,
            deadline: deadline || null,
            created_by: createdBy,
            min_quantity: parseInt(minQuantity) || 0
        });

        if (result.success) {
            showAlert('團購活動建立成功！', 'success');
            loadEvents();
        } else {
            showAlert(result.message || '建立失敗', 'error');
        }
    } catch (error) {
        console.error('建立團購活動失敗:', error);
        showAlert('系統錯誤', 'error');
    }
}

async function closeEvent(eventId) {
    if (!confirm('確定要關閉此團購活動嗎？')) return;

    try {
        const result = await api.put(`/api/events/${eventId}`, {
            status: '已截止'
        });

        if (result.success) {
            showAlert('團購活動已關閉', 'success');
            loadEvents();
        } else {
            showAlert(result.message || '操作失敗', 'error');
        }
    } catch (error) {
        console.error('關閉團購活動失敗:', error);
        showAlert('系統錯誤', 'error');
    }
}

// ========== 訂單管理 ==========

async function loadOrders() {
    const container = document.getElementById('orders-list');
    if (!container) return;

    // 取得篩選條件
    const eventId = new URLSearchParams(window.location.search).get('event_id');

    try {
        let url = '/api/orders';
        if (eventId) {
            url = `/api/events/${eventId}/orders`;
        }

        const result = await api.get(url);
        if (result.success) {
            const orders = eventId ? result.data.orders : result.data;

            if (!orders || orders.length === 0) {
                container.innerHTML = '<p>尚無訂單</p>';
                return;
            }

            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>訂單編號</th>
                            <th>訂購人</th>
                            <th>部門</th>
                            <th>飲料</th>
                            <th>杯型</th>
                            <th>甜度</th>
                            <th>冰塊</th>
                            <th>數量</th>
                            <th>總價</th>
                            <th>狀態</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            orders.forEach(order => {
                html += `
                    <tr>
                        <td>${order.order_id}</td>
                        <td>${order.customer_name}</td>
                        <td>${order.department || '-'}</td>
                        <td>${order.drink_name}</td>
                        <td>${order.size || '-'}</td>
                        <td>${order.sugar || '-'}</td>
                        <td>${order.ice || '-'}</td>
                        <td>${order.quantity}</td>
                        <td>${formatCurrency(order.total_price || 0)}</td>
                        <td>${order.status}</td>
                    </tr>
                `;
            });

            html += '</tbody></table>';

            // 顯示統計
            if (eventId && result.data.summary) {
                html += `
                    <div class="order-summary">
                        <h3>📊 訂單統計</h3>
                        <p><strong>總杯數:</strong> ${result.data.summary.total_cups} 杯</p>
                        <p class="order-total">總金額: ${formatCurrency(result.data.summary.total_amount)}</p>
                    </div>
                `;
            }

            container.innerHTML = html;
        }
    } catch (error) {
        console.error('載入訂單失敗:', error);
    }
}

function exportOrders() {
    const eventId = new URLSearchParams(window.location.search).get('event_id');
    let url = '/api/orders/export';
    if (eventId) {
        url += `?event_id=${eventId}`;
    }
    window.location.href = url;
}

// 頁面載入
document.addEventListener('DOMContentLoaded', () => {
    // 根據頁面載入對應資料
    if (document.getElementById('shops-list')) {
        loadShopsAdmin();
    }
    if (document.getElementById('events-list')) {
        loadShops('event-shop');
        loadEvents();
    }
    if (document.getElementById('orders-list')) {
        loadOrders();
    }
});
