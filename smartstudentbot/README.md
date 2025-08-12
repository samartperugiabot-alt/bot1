# SmartStudentBot 🇮🇹

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![aiogram 3](https://img.shields.io/badge/aiogram-v3-blue.svg)](https://github.com/aiogram/aiogram)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![Render](https://img.shields.io/badge/deploy%20to-Render-green.svg)](https://render.com)

**SmartStudentBot** یک ربات تلگرامی چندزبانه، رایگان و متن‌باز برای دانشجویان بین‌المللی در ایتالیا است. این ربات با تمرکز بر پروجا طراحی شده و به راحتی برای شهرهای دیگر مانند بولونیا و رم قابل گسترش است.

## ✨ ویژگی‌های اصلی

- **چندزبانه**: پشتیبانی کامل از فارسی (fa)، انگلیسی (en) و ایتالیایی (it).
- **مرکز منابع جامع**: دسترسی به ده‌ها راهنمای دسته‌بندی‌شده (اقامت، مسکن، دانشگاه و...) که از فایل‌های JSON در یک ریپازیتوری GitHub خوانده می‌شوند.
- **فرم‌های هوشمند**: فرآیندهای چندمرحله‌ای برای ثبت‌نام، محاسبه ISEE، درخواست مشاوره و...
- **یکپارچه‌سازی با سرویس‌ها**:
    - **Google Sheets**: برای ذخیره پروفایل کاربران، لاگ‌ها و سؤالات.
    - **Google Drive**: برای آپلود و مدیریت فایل‌های کاربران (رزومه، مدارک).
    - **Redis (Upstash)**: برای کش، مدیریت صف و محدودیت نرخ (Rate Limiting).
- **امن و GDPR-Friendly**: رمزنگاری داده‌های حساس، توکن امن Webhook و قابلیت حذف کامل اطلاعات کاربر (`/delete_me`).
- **مقیاس‌پذیر**: طراحی ماژولار و استفاده از فیلد `city` در داده‌ها برای گسترش آسان به شهرهای جدید بدون تغییر در کد.
- **سبک و بهینه**: طراحی شده برای اجرا روی پلن رایگان Render (512MB RAM) بدون نیاز به کتابخانه‌های سنگین AI.

## 🚀 راه‌اندازی و استقرار (Deployment)

### پیش‌نیازها

1.  **حساب Render**: برای استقرار وب‌سرویس.
2.  **حساب Google Cloud**: برای ایجاد Service Account جهت دسترسی به Sheets و Drive.
3.  **حساب Upstash**: برای ساخت یک دیتابیس رایگان Redis.
4.  **ریپازیتوری GitHub برای داده‌ها**: یک ریپازیتوری عمومی (Public) برای نگهداری فایل‌های JSON محتوایی.

### مراحل استقرار در Render

1.  **Fork این ریپازیتوری**: پروژه را در حساب GitHub خود فورک کنید.
2.  **ایجاد سرویس در Render**:
    - در داشبورد Render، روی `New +` کلیک کرده و `Web Service` را انتخاب کنید.
    - ریپازیتوری فورک‌شده خود را متصل کنید.
    - تنظیمات زیر را وارد کنید:
        - **Name**: `smartstudentbot` (یا نام دلخواه).
        - **Region**: Frankfurt (نزدیک به سرورهای تلگرام).
        - **Branch**: `main`.
        - **Build Command**: `pip install -r requirements.txt`.
        - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
3.  **تنظیم متغیرهای محیطی (Environment Variables)**:
    - به تب `Environment` در سرویس Render خود بروید.
    - تمام متغیرهای موجود در فایل `.env.example` را به عنوان `Secret` وارد کنید.
    - **نکته مهم برای `GOOGLE_CREDS_BASE64`**:
        a. فایل JSON مربوط به Service Account خود را دانلود کنید.
        b. محتوای فایل را با دستور `base64 -w 0 < your-key-file.json` (در لینوکس/مک) یا ابزارهای آنلاین به فرمت Base64 تبدیل کنید.
        c. رشته خروجی را به عنوان مقدار متغیر `GOOGLE_CREDS_BASE64` قرار دهید.
4.  **راه‌اندازی اولیه**:
    - پس از اولین استقرار موفق، ربات به طور خودکار Webhook خود را در تلگرام ثبت می‌کند.
    - آدرس `BASE_URL` شما باید `https://<your-app-name>.onrender.com` باشد.

## 🔧 توسعه محلی (Local Development)

1.  یک محیط مجازی پایتون ایجاد و فعال کنید:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  بسته‌های مورد نیاز را نصب کنید:
    ```bash
    pip install -r requirements.txt
    ```
3.  فایل `.env.example` را به `.env` کپی کرده و مقادیر آن را با اطلاعات خود پر کنید.
4.  برنامه را اجرا کنید:
    ```bash
    uvicorn main:app --reload
    ```
    **توجه**: برای دریافت آپدیت‌ها در محیط لوکال، باید از ابزاری مانند `ngrok` برای ایجاد یک تونل عمومی به `localhost:8000` خود استفاده کرده و `BASE_URL` را متناسب با آن تغییر دهید.

## 🗂️ ساختار داده‌ها در GitHub

محتوای اصلی ربات از یک ریپازیتوری جداگانه در GitHub خوانده می‌شود. ساختار پیشنهادی برای آن ریپازیتوری:

```
/data/
  /hub/
    /perugia/
      residency.json
      housing.json
      ...
    /bologna/
      residency.json
      ...
    index.json  # لیست تمام منابع در همه شهرها
  news.json
  cost_of_living.json
  ...
```

آدرس این ریپازیتوری را در متغیر `GITHUB_DATA_URL` تنظیم کنید.

## 💡 پیشنهادات برای توسعه بیشتر

- **سیستم بودجه‌بندی (`/budget`)**: ابزاری برای مدیریت هزینه‌های ماهانه دانشجو.
- **ترجمه خودکار**: یکپارچه‌سازی با سرویس‌های ترجمه رایگان مانند LibreTranslate برای پیام‌های داینامیک.
- **ابزار CLI**: توسعه `tools/cli.py` برای مدیریت داده‌ها، ارسال پیام همگانی و...
- **تست‌های کامل**: نوشتن تست‌های جامع برای تمام `handler`ها و `util`ها.
