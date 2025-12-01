/* 前端共用邏輯 */

// API 請求封裝
const api = {
    async get(url) {
        const response = await fetch(url);
        return response.json();
    },

    async post(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async put(url, data) {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async delete(url) {
        const response = await fetch(url, {
            method: 'DELETE'
        });
        return response.json();
    }
};

// 顯示提示訊息
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

// 格式化金額
function formatCurrency(amount) {
    return `$${amount.toLocaleString()}`;
}

// 格式化日期時間
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 載入飲料店列表
async function loadShops(selectId) {
    const select = document.getElementById(selectId);
    if (!select) return;

    try {
        const result = await api.get('/api/shops');
        if (result.success) {
            select.innerHTML = '<option value="">請選擇飲料店</option>';
            result.data.forEach(shop => {
                const option = document.createElement('option');
                option.value = shop.shop_id;
                option.textContent = shop.shop_name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('載入飲料店失敗:', error);
    }
}

// 載入菜單
async function loadMenu(shopId, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    try {
        container.innerHTML = '<div class="loading"><div class="loading-spinner"></div></div>';

        const result = await api.get(`/api/shops/${shopId}/menu`);
        if (result.success) {
            if (result.data.length === 0) {
                container.innerHTML = '<p>此店家尚無菜單</p>';
                return;
            }

            // 依分類分組
            const categories = {};
            result.data.forEach(item => {
                const cat = item.category || '其他';
                if (!categories[cat]) {
                    categories[cat] = [];
                }
                categories[cat].push(item);
            });

            let html = '';
            for (const [category, items] of Object.entries(categories)) {
                html += `<h3 class="card-title">${getCategoryEmoji(category)} ${category}</h3>`;
                html += '<div class="menu-grid">';
                items.forEach(item => {
                    html += `
                        <div class="menu-item" data-item-id="${item.item_id}">
                            <span class="menu-item-category">${category}</span>
                            <div class="menu-item-name">${item.name}</div>
                            <div class="menu-item-price">
                                M: ${formatCurrency(item.price_m || 0)} / L: ${formatCurrency(item.price_l || 0)}
                            </div>
                            ${item.description ? `<p>${item.description}</p>` : ''}
                        </div>
                    `;
                });
                html += '</div>';
            }

            container.innerHTML = html;
        }
    } catch (error) {
        console.error('載入菜單失敗:', error);
        container.innerHTML = '<p>載入菜單失敗，請稍後再試</p>';
    }
}

// 取得分類 Emoji
function getCategoryEmoji(category) {
    const emojis = {
        '茶類': '🍵',
        '咖啡': '☕',
        '果汁': '🍹',
        '特調': '🧋',
        '其他': '🥤'
    };
    return emojis[category] || '🥤';
}

// 頁面載入完成
document.addEventListener('DOMContentLoaded', () => {
    console.log('🍵 飲料訂購系統已載入');
});
