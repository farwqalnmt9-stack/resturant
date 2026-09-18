# سُفرة حلب

موقع مطعم Django عملي مع قائمة مرتبطة بقاعدة البيانات، سلة محفوظة في Session، طلبات، تسجيل دخول، ولوحة مخصصة لموظف التوصيل وخريطة Leaflet/OpenStreetMap لمدينة حلب.

## التشغيل من VS Code أو Conda

افتح هذا المجلد في VS Code؛ إعدادات `.vscode` تختار مفسّر Conda الجاهز تلقائياً. من **CMD** شغّل:

```bat
run-conda.bat
```

أو نفّذ مباشرة:

```bat
call C:\Users\Asus\miniconda3\Scripts\activate.bat C:\Users\Asus\miniconda3\envs\titan-gym
python manage.py runserver
```

ثم افتح `http://127.0.0.1:8000/`. لإنشاء مستخدم الإدارة:

```powershell
python manage.py createsuperuser
```

لوحة الإدارة: `http://127.0.0.1:8000/admin/`.

الدفع مضبوط على **كاش عند الاستلام** فقط. مفتاح الموقع لا يطلب إذن الموقع إلا بعد ضغط المستخدم على زر تحديد موقعي.

> ملاحظة: تعذّر إنشاء بيئة Conda جديدة داخل المجلد لأن Conda يطلب قبول شروط قنوات Anaconda أولاً. الموقع يعمل الآن عبر البيئة الموجودة `titan-gym`، وتم ربط VS Code بها. بعد قبول الشروط يمكن إنشاء بيئة مستقلة للمشروع إن رغبت.
