import pandas as pd

# 1. تحميل الملف الأساسي (اللي فيه بيانات ناقصة)
main_df = pd.read_csv('FactSale.csv')

# 2. قائمة بأسماء الملفات التانية اللي هناخد منها البيانات
other_files = ['DimCustomer.csv', 'DimStockItem.csv', 'DimDate.csv', 'DimCity.csv']

# 3. دمج الملفات واحد تلو الآخر
for file in other_files:
    other_df = pd.read_csv(file)
    
    # دمج الملفات بناءً على عمود مشترك (الـ ID مثلاً)
    # combine_first بتملا القيم الـ NaN من الملف التاني
    main_df = main_df.set_index('id').combine_first(other_df.set_index('id')).reset_index()

# 4. حفظ النتيجة النهائية في ملف جديد أو نفس الملف الخامس
main_df.to_csv('final_file.csv', index=False)

print("تم دمج البيانات وتعبئة النواقص بنجاح!")