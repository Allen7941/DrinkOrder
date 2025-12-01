# 🍵 飲料訂購系統 - 規格文件 (SPEC)

## 📋 專案概述

這是一個以**動物森友會**風格設計的**內部員工飲料團購系統**，使用 Python + Flask 作為後端框架，並使用 PostgreSQL 作為資料庫儲存，部署於 **Zeabur** 平台。

系統主要用於公司/團隊內部訂購飲料，支援多家飲料店菜單匯入，並提供管理介面讓團購發起人確認所有訂購結果。

---

## 🎯 專案目標

- 提供內部人員友善的飲料團購介面
- 支援多家飲料店菜單匯入與管理
- 採用動物森友會可愛療癒的視覺風格
- 訂單資料儲存於 PostgreSQL 資料庫
- 提供訂單彙總介面，方便團購發起人統計
- 部署於 Zeabur 平台，易於維護與擴展

---

## 🛠️ 技術架構

### 後端
| 技術 | 說明 |
|------|------|
| Python 3.11+ | 主要程式語言 |
| Flask | 輕量級 Web 框架 |
| uv | Python 套件與環境管理工具 |

### 前端
| 技術 | 說明 |
|------|------|
| HTML5 | 網頁結構 |
| CSS3 | 動物森友會風格樣式 |
| JavaScript | 互動功能 |

### 資料儲存
| 技術 | 說明 |
|------|------|
| SQLite | 本地開發用輕量資料庫 |
| PostgreSQL | 正式環境關聯式資料庫 (Zeabur) |
| SQLAlchemy | Python ORM 框架 (資料庫抽象層) |
| Flask-Migrate | 資料庫遷移工具 |

> 💡 **開發策略**：本地使用 SQLite 簡化開發流程，正式環境使用 PostgreSQL。透過 SQLAlchemy ORM 確保語法相容。

### 部署平台
| 技術 | 說明 |
|------|------|
| Zeabur | 雲端部署平台 |
| PostgreSQL (Zeabur) | Zeabur 提供的 PostgreSQL 服務 |

---

## 🎨 UI/UX 設計規範

### 動物森友會風格元素

#### 配色方案
| 用途 | 顏色 | 色碼 |
|------|------|------|
| 主色 (薄荷綠) | 背景、按鈕 | `#7FCFB5` |
| 輔色 (奶油黃) | 強調區塊 | `#F5E6C8` |
| 點綴色 (櫻花粉) | 裝飾元素 | `#FFB7C5` |
| 木質棕 | 邊框、標題 | `#8B6914` |
| 天空藍 | 次要背景 | `#87CEEB` |
| 文字色 | 主要文字 | `#5D4E37` |

#### 字型
- 標題：圓體字型（如：Noto Sans TC、jf open 粉圓）
- 內文：清晰易讀的無襯線字體

#### 視覺元素
- 圓角邊框 (border-radius: 15-20px)
- 柔和陰影效果
- 葉子、花朵、水果等裝飾圖示
- 對話框風格的提示訊息
- 可愛的動物圖示作為 Logo

---

## 📱 功能規格

### 1. 首頁 (/)
- 顯示歡迎訊息與可愛動物插圖
- 顯示目前進行中的團購活動
- 快速進入訂購頁面

### 2. 飲料店管理頁 (/admin/shops)
- 新增/編輯/刪除飲料店
- 匯入菜單功能（支援 CSV/JSON 格式）
- 管理各店家的飲料品項

### 3. 菜單頁 (/menu)
- **選擇飲料店**下拉選單
- 依選擇的店家顯示對應菜單
- 飲料分類展示
  - 茶類
  - 咖啡
  - 果汁
  - 特調
- 每個飲品顯示：
  - 名稱
  - 圖片（選用）
  - 價格
  - 簡短描述

### 4. 訂購頁 (/order)
- 訂購表單欄位：
  - 訂購人姓名 (必填)
  - 部門 (選填)
  - 飲料店選擇 (必填)
  - 飲料選擇 (必填)
  - 甜度選擇：正常/少糖/半糖/微糖/無糖
  - 冰塊選擇：正常冰/少冰/微冰/去冰/熱飲
  - 加料選項：珍珠/椰果/仙草/布丁 (+10元)
  - 杯數 (1-10)
  - 備註
- 即時計算總金額
- 送出訂單按鈕

### 5. 訂單確認頁 (/order/confirm)
- 顯示訂單摘要
- 訂單編號
- 可愛的確認動畫

### 6. 訂單彙總頁 (/admin/orders) ⭐ 管理功能
- **查看所有人的訂購結果**
- 依飲料店分類顯示
- 訂單統計：
  - 各品項數量統計
  - 各人員訂購明細
  - 總金額計算
- 篩選功能：
  - 依日期篩選
  - 依飲料店篩選
  - 依訂購人篩選
- 匯出功能（CSV/列印）
- 訂單狀態管理（待處理/已訂購/已送達）

### 7. 團購管理頁 (/admin/events) ⭐ 管理功能
- 建立新團購活動
  - 選擇飲料店
  - 設定截止時間
  - 設定最低訂購數量（選用）
- 查看進行中/已結束的團購
- 關閉/開啟團購活動

---

## 📊 資料結構

### PostgreSQL 資料表設計

#### Table: shops (飲料店)
| 欄位名稱 | 資料類型 | 說明 |
|----------|----------|------|
| shop_id | String | 店家編號 |
| shop_name | String | 店家名稱 |
| phone | String | 店家電話 |
| address | String | 店家地址 |
| is_active | Boolean | 是否啟用 |
| created_at | DateTime | 建立時間 |

#### Table: menu_items (菜單品項)
| 欄位名稱 | 資料類型 | 說明 |
|----------|----------|------|
| item_id | String | 品項編號 |
| shop_id | String | 所屬店家編號 |
| name | String | 飲料名稱 |
| category | String | 分類 (茶類/咖啡/果汁/特調) |
| price_m | Integer | M 杯價格 |
| price_l | Integer | L 杯價格 |
| description | String | 描述 |
| is_available | Boolean | 是否供應中 |

#### Table: orders (訂單)
| 欄位名稱 | 資料類型 | 說明 |
|----------|----------|------|
| order_id | String | 訂單編號 (格式: ORD-YYYYMMDD-XXXX) |
| event_id | String | 團購活動編號 |
| order_time | DateTime | 訂單時間 |
| customer_name | String | 訂購人姓名 |
| department | String | 部門 |
| shop_id | String | 飲料店編號 |
| shop_name | String | 飲料店名稱 |
| drink_name | String | 飲料名稱 |
| size | String | 杯型 (M/L) |
| sugar | String | 甜度 |
| ice | String | 冰塊 |
| toppings | String | 加料 (以逗號分隔) |
| quantity | Integer | 杯數 |
| unit_price | Integer | 單價 |
| total_price | Integer | 總價 |
| note | String | 備註 |
| status | String | 訂單狀態 (待處理/已訂購/已送達) |

#### Table: events (團購活動)
| 欄位名稱 | 資料類型 | 說明 |
|----------|----------|------|
| event_id | String | 活動編號 |
| shop_id | String | 飲料店編號 |
| shop_name | String | 飲料店名稱 |
| created_by | String | 發起人 |
| created_at | DateTime | 建立時間 |
| deadline | DateTime | 截止時間 |
| min_quantity | Integer | 最低訂購數量 |
| status | String | 狀態 (進行中/已截止/已完成) |
| total_orders | Integer | 總訂單數 |
| total_amount | Integer | 總金額 |

---

## 🔌 API 規格

### Flask 後端 API

#### 飲料店管理 API

##### GET /api/shops
取得所有飲料店
```json
{
  "success": true,
  "data": [
    {
      "shop_id": "SHOP001",
      "shop_name": "50嵐",
      "phone": "02-12345678",
      "is_active": true
    }
  ]
}
```

##### POST /api/shops
新增飲料店
```json
// Request
{
  "shop_name": "50嵐",
  "phone": "02-12345678",
  "address": "台北市信義區..."
}
```

##### POST /api/shops/{shop_id}/import-menu
匯入菜單 (支援 CSV/JSON)
```json
// Request (JSON 格式)
{
  "items": [
    {
      "name": "珍珠奶茶",
      "category": "茶類",
      "price_m": 45,
      "price_l": 55
    }
  ]
}
```

#### 菜單 API

##### GET /api/shops/{shop_id}/menu
取得指定店家菜單
```json
{
  "success": true,
  "data": [
    {
      "item_id": "ITEM001",
      "name": "珍珠奶茶",
      "category": "茶類",
      "price_m": 45,
      "price_l": 55,
      "description": "經典不敗的好味道"
    }
  ]
}
```

#### 團購活動 API

##### GET /api/events
取得團購活動列表
```json
{
  "success": true,
  "data": [
    {
      "event_id": "EVT-20251201-001",
      "shop_name": "50嵐",
      "deadline": "2025-12-01T17:00:00",
      "status": "進行中",
      "total_orders": 15
    }
  ]
}
```

##### POST /api/events
建立新團購活動
```json
// Request
{
  "shop_id": "SHOP001",
  "deadline": "2025-12-01T17:00:00",
  "min_quantity": 10,
  "created_by": "王小明"
}
```

#### 訂單 API

##### POST /api/orders
新增訂單
```json
// Request
{
  "event_id": "EVT-20251201-001",
  "customer_name": "小明",
  "department": "研發部",
  "shop_id": "SHOP001",
  "drink_id": "ITEM001",
  "size": "L",
  "sugar": "半糖",
  "ice": "少冰",
  "toppings": ["珍珠"],
  "quantity": 2,
  "note": ""
}

// Response
{
  "success": true,
  "order_id": "ORD-20251201-0001",
  "message": "訂單已成功送出！"
}
```

##### GET /api/events/{event_id}/orders
取得團購活動的所有訂單（管理用）
```json
{
  "success": true,
  "data": {
    "event_id": "EVT-20251201-001",
    "shop_name": "50嵐",
    "orders": [
      {
        "order_id": "ORD-20251201-0001",
        "customer_name": "小明",
        "department": "研發部",
        "drink_name": "珍珠奶茶",
        "size": "L",
        "sugar": "半糖",
        "ice": "少冰",
        "quantity": 2,
        "total_price": 110
      }
    ],
    "summary": {
      "total_cups": 25,
      "total_amount": 1250,
      "items_count": {
        "珍珠奶茶-L-半糖-少冰": 5,
        "紅茶拿鐵-M-正常-正常冰": 3
      }
    }
  }
}
```

##### GET /api/orders/export?event_id={event_id}
匯出訂單（CSV 格式）

---

## 📁 專案結構

```
DrinkOrder/
├── pyproject.toml          # uv 專案設定
├── uv.lock                  # 依賴鎖定檔
├── SPEC.md                  # 規格文件 (本文件)
├── README.md                # 專案說明
├── .env                     # 環境變數 (本地開發)
├── .gitignore               # Git 忽略檔案 (含 .env, instance/, __pycache__)
│
├── app/
│   ├── __init__.py          # Flask 應用程式初始化
│   ├── config.py            # 設定檔
│   ├── models.py            # SQLAlchemy 資料模型
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # 主要頁面路由
│   │   ├── api.py           # API 路由
│   │   └── admin.py         # 管理頁面路由
│   ├── services/
│   │   ├── __init__.py
│   │   ├── shop_service.py  # 飲料店服務
│   │   ├── order_service.py # 訂單服務
│   │   └── event_service.py # 團購活動服務
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # 動物森友會風格樣式
│   │   ├── js/
│   │   │   ├── main.js      # 前端共用邏輯
│   │   │   ├── order.js     # 訂購頁邏輯
│   │   │   └── admin.js     # 管理頁邏輯
│   │   └── images/
│   │       ├── logo.png     # Logo
│   │       └── decorations/ # 裝飾圖片
│   └── templates/
│       ├── base.html        # 基礎模板
│       ├── index.html       # 首頁
│       ├── menu.html        # 菜單頁
│       ├── order.html       # 訂購頁
│       ├── confirm.html     # 確認頁
│       └── admin/
│           ├── shops.html       # 飲料店管理
│           ├── import_menu.html # 匯入菜單
│           ├── events.html      # 團購活動管理
│           └── orders.html      # 訂單彙總
│
├── data/
│   └── sample_menu.json     # 範例菜單資料
│
├── instance/
│   └── drink_order.db       # SQLite 資料庫 (本地開發，git ignore)
│
├── migrations/              # 資料庫遷移檔案
│
└── zeabur.json              # Zeabur 部署設定
```

---

## 🚀 開發里程碑

### Phase 1 - 基礎建設
- [ ] 專案初始化 (uv + Flask)
- [ ] 基礎路由設定
- [ ] 模板結構建立
- [ ] PostgreSQL 資料庫模型設計
- [ ] SQLAlchemy ORM 設定

### Phase 2 - 前端開發
- [ ] 動物森友會風格 CSS
- [ ] 首頁設計
- [ ] 菜單頁設計（支援多店家切換）
- [ ] 訂購表單頁設計
- [ ] 響應式設計

### Phase 3 - 管理功能開發 ⭐
- [ ] 飲料店管理頁面
- [ ] 菜單匯入功能 (CSV/JSON)
- [ ] 團購活動管理
- [ ] 訂單彙總頁面
- [ ] 訂單統計與匯出

### Phase 4 - 後端整合
- [ ] 完整 API 開發
- [ ] 資料庫遷移設定 (Flask-Migrate)
- [ ] 錯誤處理
- [ ] 資料驗證

### Phase 5 - 測試與部署
- [ ] 功能測試
- [ ] UI/UX 優化
- [ ] 效能優化
- [ ] Zeabur 部署設定
- [ ] PostgreSQL 連線設定
- [ ] 正式上線

---

## 🔧 環境變數

### 本地開發環境 (.env)
```env
# .env 檔案 (本地開發)
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here

# 本地使用 SQLite (不需設定 DATABASE_URL，系統會自動使用 SQLite)
# DATABASE_URL=sqlite:///drink_order.db
```

### 正式環境 (Zeabur)
```env
# Zeabur 會自動注入 PostgreSQL 連線
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://username:password@host:port/database
```

### Zeabur 環境變數設定
| 變數名稱 | 說明 | 必填 |
|----------|------|------|
| SECRET_KEY | Flask 密鑰 (請使用強密碼) | ✅ |
| DATABASE_URL | PostgreSQL 連線字串 (Zeabur 自動注入) | ✅ (自動) |
| FLASK_ENV | 設為 `production` | 建議 |

---

## 📝 飲料菜單 (範例資料 - 50嵐)

### 茶類
| 品名 | M 價格 | L 價格 |
|------|--------|--------|
| 珍珠奶茶 | 45 | 55 |
| 紅茶拿鐵 | 50 | 60 |
| 四季春茶 | 30 | 40 |
| 烏龍綠茶 | 35 | 45 |
| 冬瓜茶 | 30 | 40 |

### 咖啡
| 品名 | M 價格 | L 價格 |
|------|--------|--------|
| 美式咖啡 | 45 | 55 |
| 拿鐵咖啡 | 55 | 65 |
| 摩卡咖啡 | 60 | 70 |
| 焦糖瑪奇朵 | 65 | 75 |

### 果汁
| 品名 | M 價格 | L 價格 |
|------|--------|--------|
| 新鮮柳橙汁 | 55 | 65 |
| 芒果冰沙 | 60 | 70 |
| 西瓜汁 | 50 | 60 |
| 蘋果汁 | 50 | 60 |

### 特調
| 品名 | M 價格 | L 價格 |
|------|--------|--------|
| 百香果多多 | 50 | 60 |
| 葡萄柚綠茶 | 50 | 60 |
| 芒果青茶 | 55 | 65 |
| 草莓奶霜 | 65 | 75 |

---

## 📥 菜單匯入格式

### CSV 格式範例
```csv
name,category,price_m,price_l,description
珍珠奶茶,茶類,45,55,經典不敗的好味道
紅茶拿鐵,茶類,50,60,香濃紅茶搭配鮮奶
美式咖啡,咖啡,45,55,純粹咖啡香
```

### JSON 格式範例
```json
{
  "items": [
    {
      "name": "珍珠奶茶",
      "category": "茶類",
      "price_m": 45,
      "price_l": 55,
      "description": "經典不敗的好味道"
    }
  ]
}
```

---

## 🎮 動物森友會元素設計參考

### 介面元素
1. **對話框樣式**：類似遊戲中 NPC 對話框的圓角矩形
2. **按鈕設計**：帶有木質紋理或葉子圖案的圓角按鈕
3. **載入動畫**：飛舞的樹葉或跳躍的小動物
4. **成功提示**：類似遊戲中完成任務的金幣/星星動畫
5. **背景音效**：(選用) 輕快的背景音樂

### 裝飾元素
- 🍃 樹葉
- 🌸 櫻花
- 🍎 蘋果
- 🦝 狸克 (Tom Nook) 風格的角色
- 🏠 小木屋圖案
- 💰 鈴錢袋

---

## 📌 注意事項

1. **資料庫連線**：正式環境使用連線池管理 PostgreSQL 連線
2. **資料驗證**：前後端都需進行表單驗證
3. **錯誤處理**：提供友善的錯誤訊息
4. **手機優化**：確保行動裝置良好體驗
5. **安全性**：敏感資訊存放於環境變數
6. **資料庫遷移**：使用 Flask-Migrate 管理 schema 變更
7. **資料庫相容性**：全部使用 SQLAlchemy ORM，避免原生 SQL 確保 SQLite/PostgreSQL 相容

---

## 🔄 SQLite / PostgreSQL 相容性指南

### ✅ 可安全使用的功能
| 功能 | 說明 |
|------|------|
| 基本 CRUD | 新增、讀取、更新、刪除 |
| 關聯查詢 | JOIN, relationship |
| 過濾排序 | filter, order_by |
| 聚合函數 | count, sum, avg |
| 交易控制 | commit, rollback |

### ⚠️ 避免使用的功能
| 功能 | 原因 |
|------|------|
| 原生 SQL | 語法可能不相容 |
| ARRAY 欄位 | SQLite 不支援 |
| JSONB 進階查詢 | SQLite 支援有限 |
| 全文搜尋 | 實作方式不同 |

### 💡 開發建議
```python
# ✅ 正確：使用 ORM
orders = Order.query.filter_by(status='待處理').all()

# ❌ 避免：原生 SQL
db.session.execute('SELECT * FROM orders WHERE status = "待處理"')
```

---

## 📚 參考資源

- [Flask 官方文件](https://flask.palletsprojects.com/)
- [uv 官方文件](https://docs.astral.sh/uv/)
- [SQLAlchemy 官方文件](https://docs.sqlalchemy.org/)
- [Flask-Migrate 文件](https://flask-migrate.readthedocs.io/)
- [Zeabur 官方文件](https://zeabur.com/docs)
- [PostgreSQL 文件](https://www.postgresql.org/docs/)
- [動物森友會色彩參考](https://animalcrossing.fandom.com/)

---

*最後更新：2025年12月1日*
