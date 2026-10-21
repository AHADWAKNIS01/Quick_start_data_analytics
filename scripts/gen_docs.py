import json, os, pandas as pd
from datetime import datetime, timezone

INPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample')
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(OUTPUT, exist_ok=True)

orders = pd.read_csv(f'{INPUT}/orders.csv')
products = pd.read_csv(f'{INPUT}/products.csv')
departments = pd.read_csv(f'{INPUT}/departments.csv')
prior = pd.read_csv(f'{INPUT}/order_products__prior.csv')
train = pd.read_csv(f'{INPUT}/order_products__train.csv')

lines = pd.concat([prior, train], ignore_index=True)
joined = lines.merge(orders, on='order_id').merge(products, on='product_id').merge(departments, on='department_id', how='left')

kpis = {
    'orders': int(joined['order_id'].nunique()),
    'customers': int(joined['user_id'].nunique()),
    'items': int(len(joined)),
    'reorder_rate': float(joined['reordered'].mean()),
}
hourly = joined.groupby('order_hour_of_day').size().reset_index(name='items').sort_values('order_hour_of_day')
days = joined.groupby('order_dow').size().reset_index(name='items').sort_values('order_dow')
depts = joined.groupby(['department_id','department']).agg(items=('order_id','count'), reorder_rate=('reordered','mean')).reset_index().sort_values('items', ascending=False)
prods = joined.groupby(['product_id','product_name','department_id','department']).agg(items=('order_id','count'), reorder_rate=('reordered','mean')).reset_index().sort_values('items', ascending=False).head(20)

meta = {'dataset': 'sample', 'generated_at': datetime.now(timezone.utc).isoformat(), 'source': 'Instacart 2017', 'batch_type': 'pandas local'}

docs = {
    'metadata': meta,
    'kpis': kpis,
    'hourly': {'dataset': 'sample', 'data': hourly.to_dict(orient='records')},
    'days': {'dataset': 'sample', 'data': days.to_dict(orient='records')},
    'departments': {'dataset': 'sample', 'data': depts.to_dict(orient='records')},
    'products': {'dataset': 'sample', 'data': prods.to_dict(orient='records')},
}

with open(f'{OUTPUT}/docs.json', 'w') as f:
    json.dump(docs, f)

print('docs.json written to', OUTPUT)
print('KPIs:', kpis)
