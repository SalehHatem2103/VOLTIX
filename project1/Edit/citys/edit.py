import pandas as pd
import numpy as np

# 1. تحميل الملف
df = pd.read_csv('DimCity.csv')

# 2. تحويل الأصفار إلى NaN مؤقتاً لسهولة التعامل معها إحصائياً
df['Latest Recorded Population'] = df['Latest Recorded Population'].replace(0, np.nan)

# 3. حساب "الوسيط" (Median) لكل ولاية
# استخدمنا الوسيط لأنه أدق من المتوسط في حالة وجود مدن ضخمة جداً (مثل LA) 
# لكي لا ترفع الأرقام بشكل غير واقعي للقرى الصغيرة
state_medians = df.groupby('State Province')['Latest Recorded Population'].transform('median')

# 4. ملء القيم المفقودة (التي كانت صفراً) بمتوسط الولاية التابعة لها
df['Latest Recorded Population'] = df['Latest Recorded Population'].fillna(state_medians)

# 5. إذا بقيت أي مدينة (في حال كانت ولاية كاملة أصفاراً - وهذا نادر)، نضع المتوسط العام
overall_median = df['Latest Recorded Population'].median()
df['Latest Recorded Population'] = df['Latest Recorded Population'].fillna(overall_median)

# 6. تحويل الأرقام إلى أرقام صحيحة (Integer)
df['Latest Recorded Population'] = df['Latest Recorded Population'].astype(int)

# 7. حفظ الملف النهائي
df.to_csv('DimCity_Fully_Fixed.csv', index=False)

print("تمت العملية بنجاح!")
print(f"عدد القيم الصفرية المتبقية: {(df['Latest Recorded Population'] == 0).sum()}")