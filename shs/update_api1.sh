#!/bin/bash
set -e  # إيقاف التنفيذ عند حدوث أي خطأ

# تحديد المسارات
HOME_DIR="$HOME"
TARGET_DIR="$HOME_DIR/pybot/new/newapi"
TEMP_DIR="$HOME_DIR/newapi_x"
REPO_URL="https://github.com/MrIbrahem/newapi.git"
PYTHON_BIN="$HOME_DIR/local/bin/python3"

cd "$HOME" || exit 1

# إزالة أي مجلد مؤقت قديم
rm -rf "$TEMP_DIR"

# إنشاء المجلدات إذا لم تكن موجودة
mkdir -p "$TARGET_DIR"

# استنساخ المستودع إلى المجلد المؤقت
git clone "$REPO_URL" "$TEMP_DIR"

# نسخ الملفات من المجلد المؤقت إلى الوجهة
cp -rf "$TEMP_DIR"/* "$TARGET_DIR" -v

# حذف ملفات الـ .pyc غير الضرورية
find "$TARGET_DIR" -name "*.pyc" -exec rm -f {} +

# ضبط الصلاحيات (عدم تغيير ملفات .pyc)
find "$TARGET_DIR" -type f ! -name "*.pyc" -exec chmod 6770 {} \;

# حذف المجلد المؤقت بعد الانتهاء
rm -rf "$TEMP_DIR"

# تثبيت المتطلبات
"$PYTHON_BIN" -m pip install -r "$TARGET_DIR/requirements.in" -U

echo "Script executed successfully."
