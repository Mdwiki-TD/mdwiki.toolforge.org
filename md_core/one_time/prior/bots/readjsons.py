import os
from pathlib import Path
import json

# استدعاء الدالة وتمرير المجلد الحالي كوسيطة
folder_path = Path(__file__).parent

# قم بعمل سكان للمجلد ومجلداته الفرعية
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.json'):  # فقط الملفات بامتداد .json
            file_path = os.path.join(root, file_name)
            print("path:", file_path)

            # قراءة الملف كـ JSON
            with open(file_path) as file:
                json_data = file.read()

            # طباعة حجم الملف قبل التعديل
            file_size_before = os.path.getsize(file_path)
            print("size before: ", file_size_before)

            # كتابة الملف بدون تنسيق
            with open(file_path, 'w') as file:
                json.dump(json.loads(json_data), file)

            # طباعة حجم الملف بعد التعديل
            file_size_after = os.path.getsize(file_path)
            print("size after:", file_size_after)
            print("--------------------")
            print("Difference:", file_size_after - file_size_before)
