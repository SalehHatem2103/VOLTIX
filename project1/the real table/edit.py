import pandas as pd

df = pd.read_csv('FactSale_final.csv')

# ترتيب الأعمدة الجديد
cols = [
    'Sale Key', 'City Key', 'City', 'State Province', 'Country',
    'Customer Key', 'Bill To Customer Key', 'Stock Item Key',
    'Invoice Date Key', 'Delivery Date Key', 'Salesperson Key',
    'WWI Invoice ID', 'Description', 'Package', 'Quantity',
    'Unit Price', 'Tax Rate', 'Total Excluding Tax', 'Tax Amount',
    'Profit', 'Total Including Tax', 'Total Dry Items',
    'Total Chiller Items', 'Lineage Key'
]

df = df[cols]
df.to_csv('FactSale_final1.csv', index=False)
print(df.columns.tolist())