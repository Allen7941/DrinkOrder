# 🍵 狸克飲料舖 - 飲料訂購系統

一個以**動物森友會**風格設計的內部員工飲料團購系統，使用 Python + Flask 開發。

## ✨ 功能特色

- 🦝 動物森友會風格的可愛介面
- 🏪 多家飲料店菜單管理
- 🎉 團購活動建立與管理
- 🛒 友善的訂購介面
- 📊 訂單彙總與統計
- 📥 訂單匯出 (CSV)

## 🛠️ 技術架構

- **後端**: Python 3.11+ / Flask
- **資料庫**: SQLite (開發) / PostgreSQL (正式)
- **ORM**: SQLAlchemy + Flask-Migrate
- **套件管理**: uv

## 🚀 快速開始

### 1. 安裝 uv (如果尚未安裝)

```powershell
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 建立虛擬環境並安裝依賴

```bash
# 進入專案目錄
cd DrinkOrder

# 使用 uv 同步依賴
uv sync
```

### 3. 執行開發伺服器

```bash
# 啟動 Flask 開發伺服器
uv run flask run

# 或指定 port
uv run flask run --port 5000
```

### 4. 開啟瀏覽器

前往 http://localhost:5000 即可看到系統首頁！

## 📁 專案結構

```
DrinkOrder/
├── pyproject.toml          # uv 專案設定
├── .env                    # 環境變數 (本地開發)
├── app/
│   ├── __init__.py         # Flask 應用程式初始化
│   ├── config.py           # 設定檔
│   ├── models.py           # SQLAlchemy 資料模型
│   ├── routes/             # 路由
│   │   ├── main.py         # 主要頁面路由
│   │   ├── api.py          # API 路由
│   │   └── admin.py        # 管理頁面路由
│   ├── services/           # 業務邏輯層
│   ├── static/             # 靜態資源
│   │   ├── css/style.css   # 動物森友會風格樣式
│   │   └── js/             # JavaScript
│   └── templates/          # Jinja2 模板
└── instance/               # SQLite 資料庫 (自動產生)
```

## 🎨 動物森友會風格

- 薄荷綠 `#7FCFB5` - 主色調
- 奶油黃 `#F5E6C8` - 輔色
- 櫻花粉 `#FFB7C5` - 點綴色
- 木質棕 `#8B6914` - 標題邊框

## 📝 範例菜單資料

在店家管理頁面，可以使用 JSON 格式匯入菜單：

```json
{
  "items": [
    {"name": "珍珠奶茶", "category": "茶類", "price_m": 45, "price_l": 55, "description": "經典不敗的好味道"},
    {"name": "紅茶拿鐵", "category": "茶類", "price_m": 50, "price_l": 60, "description": "香濃紅茶搭配鮮奶"},
    {"name": "美式咖啡", "category": "咖啡", "price_m": 45, "price_l": 55, "description": "純粹咖啡香"}
  ]
}
```

## 🚀 部署到 Zeabur

1. 在 Zeabur 建立新專案
2. 連結 GitHub 儲存庫
3. 新增 PostgreSQL 服務
4. 設定環境變數：
   - `SECRET_KEY`: 強密碼
   - `FLASK_ENV`: production
5. 部署完成！

## 📄 授權

MIT License

---

🍃 Made with ❤️ by 狸克飲料舖團隊
