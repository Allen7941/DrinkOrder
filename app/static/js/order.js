/* 訂購頁邏輯 */

let selectedDrink = null;
let selectedSize = 'M';
let selectedSugar = '正常';
let selectedIce = '正常冰';
let selectedToppings = [];
let quantity = 1;

// 初始化訂購頁
document.addEventListener('DOMContentLoaded', () => {
    // 載入飲料店
    loadShops('shop-select');

    // 監聽飲料店選擇
    const shopSelect = document.getElementById('shop-select');
    if (shopSelect) {
        shopSelect.addEventListener('change', (e) => {
            if (e.target.value) {
                loadMenuForOrder(e.target.value);
            }
        });
    }

    // 初始化選項按鈕
    initOptionButtons();

    // 初始化數量選擇器
    initQuantitySelector();

    // 初始化加料選項
    initToppings();

    // 初始化訂購表單
    initOrderForm();
});

// 載入訂購用菜單
async function loadMenuForOrder(shopId) {
    const container = document.getElementById('drink-menu');
    if (!container) return;

    try {
        container.innerHTML = '<div class="loading"><div class="loading-spinner"></div></div>';

        const result = await api.get(`/api/shops/${shopId}/menu`);
        if (result.success) {
            if (result.data.length === 0) {
                container.innerHTML = '<p>此店家尚無菜單</p>';
                return;
            }

            let html = '<div class="menu-grid">';
            result.data.forEach(item => {
                html += `
                    <div class="menu-item" data-item='${JSON.stringify(item)}' onclick="selectDrink(this)">
                        <span class="menu-item-category">${item.category || '其他'}</span>
                        <div class="menu-item-name">${item.name}</div>
                        <div class="menu-item-price">
                            M: ${formatCurrency(item.price_m || 0)} / L: ${formatCurrency(item.price_l || 0)}
                        </div>
                    </div>
                `;
            });
            html += '</div>';

            container.innerHTML = html;
        }
    } catch (error) {
        console.error('載入菜單失敗:', error);
        container.innerHTML = '<p>載入菜單失敗，請稍後再試</p>';
    }
}

// 選擇飲料
function selectDrink(element) {
    // 移除之前的選擇
    document.querySelectorAll('.menu-item').forEach(el => {
        el.classList.remove('active');
        el.style.borderColor = 'transparent';
    });

    // 設定新選擇
    element.classList.add('active');
    element.style.borderColor = '#7FCFB5';

    selectedDrink = JSON.parse(element.dataset.item);

    // 更新價格
    updateTotalPrice();
}

// 初始化選項按鈕
function initOptionButtons() {
    // 杯型選擇
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedSize = btn.dataset.value;
            updateTotalPrice();
        });
    });

    // 甜度選擇
    document.querySelectorAll('.sugar-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.sugar-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedSugar = btn.dataset.value;
        });
    });

    // 冰塊選擇
    document.querySelectorAll('.ice-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.ice-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedIce = btn.dataset.value;
        });
    });
}

// 初始化數量選擇器
function initQuantitySelector() {
    const minusBtn = document.getElementById('quantity-minus');
    const plusBtn = document.getElementById('quantity-plus');
    const quantityDisplay = document.getElementById('quantity-value');

    if (minusBtn) {
        minusBtn.addEventListener('click', () => {
            if (quantity > 1) {
                quantity--;
                quantityDisplay.textContent = quantity;
                updateTotalPrice();
            }
        });
    }

    if (plusBtn) {
        plusBtn.addEventListener('click', () => {
            if (quantity < 10) {
                quantity++;
                quantityDisplay.textContent = quantity;
                updateTotalPrice();
            }
        });
    }
}

// 初始化加料選項
function initToppings() {
    document.querySelectorAll('.topping-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            selectedToppings = [];
            document.querySelectorAll('.topping-checkbox:checked').forEach(cb => {
                selectedToppings.push(cb.value);
            });
            updateTotalPrice();
        });
    });
}

// 更新總價
function updateTotalPrice() {
    if (!selectedDrink) return;

    let unitPrice = selectedSize === 'L' ? (selectedDrink.price_l || 0) : (selectedDrink.price_m || 0);
    let toppingPrice = selectedToppings.length * 10;
    let totalPrice = (unitPrice + toppingPrice) * quantity;

    const totalDisplay = document.getElementById('total-price');
    if (totalDisplay) {
        totalDisplay.textContent = formatCurrency(totalPrice);
    }

    const summaryDisplay = document.getElementById('order-summary-text');
    if (summaryDisplay) {
        summaryDisplay.innerHTML = `
            <p><strong>飲料:</strong> ${selectedDrink.name}</p>
            <p><strong>杯型:</strong> ${selectedSize} | <strong>甜度:</strong> ${selectedSugar} | <strong>冰塊:</strong> ${selectedIce}</p>
            ${selectedToppings.length > 0 ? `<p><strong>加料:</strong> ${selectedToppings.join(', ')} (+$${selectedToppings.length * 10})</p>` : ''}
            <p><strong>數量:</strong> ${quantity} 杯</p>
        `;
    }
}

// 初始化訂購表單
function initOrderForm() {
    const form = document.getElementById('order-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const customerName = document.getElementById('customer-name').value;
        const department = document.getElementById('department').value;
        const note = document.getElementById('note').value;
        const shopSelect = document.getElementById('shop-select');

        if (!customerName) {
            showAlert('請輸入訂購人姓名', 'error');
            return;
        }

        if (!selectedDrink) {
            showAlert('請選擇飲料', 'error');
            return;
        }

        const orderData = {
            customer_name: customerName,
            department: department,
            shop_id: shopSelect.value,
            shop_name: shopSelect.options[shopSelect.selectedIndex].text,
            drink_id: selectedDrink.item_id,
            drink_name: selectedDrink.name,
            size: selectedSize,
            sugar: selectedSugar,
            ice: selectedIce,
            toppings: selectedToppings,
            quantity: quantity,
            note: note
        };

        try {
            const result = await api.post('/api/orders', orderData);
            if (result.success) {
                // 儲存訂單資訊到 sessionStorage
                sessionStorage.setItem('lastOrder', JSON.stringify({
                    ...orderData,
                    order_id: result.order_id,
                    total_price: calculateTotalPrice()
                }));

                // 跳轉到確認頁
                window.location.href = '/order/confirm';
            } else {
                showAlert(result.message || '訂單送出失敗', 'error');
            }
        } catch (error) {
            console.error('訂單送出錯誤:', error);
            showAlert('系統錯誤，請稍後再試', 'error');
        }
    });
}

// 計算總價
function calculateTotalPrice() {
    if (!selectedDrink) return 0;
    let unitPrice = selectedSize === 'L' ? (selectedDrink.price_l || 0) : (selectedDrink.price_m || 0);
    let toppingPrice = selectedToppings.length * 10;
    return (unitPrice + toppingPrice) * quantity;
}
