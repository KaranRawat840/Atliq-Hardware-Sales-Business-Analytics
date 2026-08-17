# %%
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
# %%
engine = create_engine("mysql+pymysql://root:root@localhost/gdb023")
# %%
df_customer    = pd.read_sql("SELECT * FROM dim_customer", engine)
df_product     = pd.read_sql("SELECT * FROM dim_product", engine)
df_gross_price = pd.read_sql("SELECT * FROM fact_gross_price", engine)
df_manu_cost   = pd.read_sql("SELECT * FROM fact_manufacturing_cost", engine)
df_pre_inv     = pd.read_sql("SELECT * FROM fact_pre_invoice_deductions", engine)
df_sales       = pd.read_sql("SELECT * FROM fact_sales_monthly", engine)
# %% [markdown]
# ### **Q.1 Identify the markets in which the customer "Atliq Exclusive" operates its business in the APAC region. Present the findings in an insightful way.**
# %%
markets = df_customer[(df_customer.customer == 'Atliq Exclusive') & (df_customer.region == 'APAC')]['market'].unique()
print(markets)
# %% [markdown]
# ### **Q.2 Compare the unique product counts between 2020 and 2021. Calculate the percentage change and present the analysis.**
# %% [markdown]
# CODE:
# %%
counts = df_sales.groupby('fiscal_year')['product_code'].nunique()
pct_change = (counts[2021] - counts[2020]) / counts[2020] * 100
print(counts, pct_change)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
counts = df_sales.groupby('fiscal_year')['product_code'].nunique()

fig, ax = plt.subplots(figsize=(5,4))
bars = ax.bar(counts.index.astype(str), counts.values, color=['#A9CCE3', '#2E5EAA'])
ax.set_title('Unique Products Sold: 2020 vs 2021')
ax.set_ylabel('Unique Product Count')
for b in bars:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+2, str(int(b.get_height())),
            ha='center', fontweight='bold')
plt.show()
# %% [markdown]
# ### **Q.3 Analyze the unique product counts for each segment. The results should be sorted in descending order of their counts.**
# %% [markdown]
# CODE:
# %%
seg_counts = df_product.groupby('segment')['product_code'].nunique().sort_values(ascending=False)
print(seg_counts)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
seg_counts = df_product.groupby('segment')['product_code'].nunique() \
                        .sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(7,4))
ax.barh(seg_counts.index, seg_counts.values, color='#2E5EAA')
ax.set_title('Unique Product Count by Segment')
ax.set_xlabel('Number of Unique Products')
plt.tight_layout()
plt.show()
# %% [markdown]
# ### **Q.4 Determine which segment had the most significant increase in unique products from 2020 to 2021.**
# %% [markdown]
# CODE:
# %%
merged = df_sales.merge(df_product, on='product_code')
pivot = merged.groupby(['segment', 'fiscal_year'])['product_code'].nunique().unstack()
pivot['increase'] = pivot[2021] - pivot[2020]
pivot.sort_values('increase', ascending=False)
print(merged, pivot)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
merged = df_sales.merge(df_product, on='product_code')
pivot = merged.groupby(['segment','fiscal_year'])['product_code'].nunique().unstack().sort_values(2021, ascending=False)

pivot.plot(kind='bar', figsize=(8,4.5), color=['#A9CCE3','#2E5EAA'])
plt.title('Unique Products by Segment: 2020 vs 2021')
plt.ylabel('Unique Product Count')
plt.xticks(rotation=30, ha='right')
plt.legend(title='Fiscal Year')
plt.tight_layout()
plt.show()
# %% [markdown]
# ### **Q.4 Identify the products with the highest and lowest manufacturing costs. Include their respective details and highlight the findings.**
# %% [markdown]
# CODE:
# %%
merged = df_manu_cost.merge(df_product, on='product_code')
top5 = merged.sort_values('manufacturing_cost', ascending=False).head(5)
bottom5 = merged.sort_values('manufacturing_cost', ascending=True).head(5)
print(top5, bottom5)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
merged = df_manu_cost.merge(df_product, on='product_code')
top5 = merged.sort_values('manufacturing_cost', ascending=False).head(5)
bottom5 = merged.sort_values('manufacturing_cost', ascending=True).head(5)

fig, axes = plt.subplots(1, 2, figsize=(11,4))
axes[0].barh(top5['product'] + ' (' + top5['variant'] + ')', top5['manufacturing_cost'], color='#C0392B')
axes[0].set_title('Top 5 Highest Manufacturing Cost')
axes[0].invert_yaxis()

axes[1].barh(bottom5['product'] + ' (' + bottom5['variant'] + ')', bottom5['manufacturing_cost'], color='#2E7D32')
axes[1].set_title('Top 5 Lowest Manufacturing Cost')
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()
# %% [markdown]
# ### **Q.6 Analyze the top 5 customers who received the highest average pre-invoice discount percentage for the fiscal year 2021 and in the Indian market.**
# %% [markdown]
# CODE:
# %%
merged = df_pre_inv.merge(df_customer, on='customer_code')
filtered = merged[(merged.fiscal_year == 2021) & (merged.market == 'India')]
top5 = filtered.groupby('customer')['pre_invoice_discount_pct'].mean().sort_values(ascending=True).tail(5)
print(top5)
# %% [markdown]
# VISUAL REPRESENTAION:
# %%
merged = df_pre_inv.merge(df_customer, on='customer_code')
filtered = merged[(merged.fiscal_year == 2021) & (merged.market == 'India')]
top5 = filtered.groupby('customer')['pre_invoice_discount_pct'].mean().sort_values(ascending=True).tail(5)

fig, ax = plt.subplots(figsize=(7,4))
bars = ax.barh(top5.index, top5.values*100, color='#2E5EAA')
ax.set_title('Top 5 Customers by Avg. Pre-Invoice Discount % (India, FY2021)')
ax.set_xlabel('Discount %')
for b in bars:
    ax.text(b.get_width()+0.2, b.get_y()+b.get_height()/2, f'{b.get_width():.1f}%', va='center')
plt.tight_layout()
plt.show()
# %% [markdown]
# 
# ### **Q.7 Create a table of the Gross sales amount for the customer “Atliq Exclusive” for each month. This analysis helps to get an idea of low and high-performing months and take strategic decisions. The final table  contains these columns:**
# 
# **• Month
# • Year
# • Gross sales**
# %% [markdown]
# CODE:
# %%
merged = (df_sales.merge(df_customer, on='customer_code').merge(df_gross_price, on=['product_code','fiscal_year']))
atliq = merged[merged.customer == 'Atliq Exclusive'].copy()
atliq['gross_sales'] = atliq['sold_quantity'] * atliq['gross_price']
atliq['date'] = pd.to_datetime(atliq['date'])
monthly = atliq.groupby('date')['gross_sales'].sum() / 1e6
print(monthly)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
merged = (df_sales.merge(df_customer, on='customer_code').merge(df_gross_price, on=['product_code','fiscal_year']))
atliq = merged[merged.customer == 'Atliq Exclusive'].copy()
atliq['gross_sales'] = atliq['sold_quantity'] * atliq['gross_price']
atliq['date'] = pd.to_datetime(atliq['date'])
monthly = atliq.groupby('date')['gross_sales'].sum() / 1e6

fig, ax = plt.subplots(figsize=(9,4))
ax.plot(monthly.index, monthly.values, marker='o', color='#2E5EAA')
ax.fill_between(monthly.index, monthly.values, alpha=0.1, color='#2E5EAA')
ax.set_title('Atliq Exclusive Monthly Gross Sales')
ax.set_ylabel('Gross Sales ($M)')
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
# %% [markdown]
# ### **Q.8 Which quarter of 2020, got the maximum total_sold_quantity?**
# %% [markdown]
# CODE:
# %%
df_sales['date'] = pd.to_datetime(df_sales['date'])
fy2020 = df_sales[df_sales.fiscal_year == 2020].copy()

def fiscal_quarter(d):
    m = d.month
    if m in [9,10,11]: return 'Q1\n(Sep-Nov)'
    if m in [12,1,2]:  return 'Q2\n(Dec-Feb)'
    if m in [3,4,5]:   return 'Q3\n(Mar-May)'
    return 'Q4\n(Jun-Aug)'

fy2020['quarter'] = fy2020['date'].apply(fiscal_quarter)
by_q = fy2020.groupby('quarter')['sold_quantity'].sum()
order = ['Q1\n(Sep-Nov)','Q2\n(Dec-Feb)','Q3\n(Mar-May)','Q4\n(Jun-Aug)']
by_q = by_q.reindex(order)
print(by_q)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
df_sales['date'] = pd.to_datetime(df_sales['date'])
fy2020 = df_sales[df_sales.fiscal_year == 2020].copy()

def fiscal_quarter(d):
    m = d.month
    if m in [9,10,11]: return 'Q1\n(Sep-Nov)'
    if m in [12,1,2]:  return 'Q2\n(Dec-Feb)'
    if m in [3,4,5]:   return 'Q3\n(Mar-May)'
    return 'Q4\n(Jun-Aug)'

fy2020['quarter'] = fy2020['date'].apply(fiscal_quarter)
by_q = fy2020.groupby('quarter')['sold_quantity'].sum()
order = ['Q1\n(Sep-Nov)','Q2\n(Dec-Feb)','Q3\n(Mar-May)','Q4\n(Jun-Aug)']
by_q = by_q.reindex(order)

fig, ax = plt.subplots(figsize=(7,4))
colors = ['#2E5EAA' if v == by_q.max() else '#A9CCE3' for v in by_q.values]
ax.bar(by_q.index, by_q.values, color=colors)
ax.set_title('Total Sold Quantity by Fiscal Quarter, FY2020')
ax.set_ylabel('Units Sold')
plt.tight_layout()
plt.show()
# %% [markdown]
# ### **Q.9 Determine which channel contributed the most to gross sales in FY 2021 and calculate its percentage contribution.**
# %% [markdown]
# CODE:
# %%
merged = (df_sales.merge(df_customer, on='customer_code').merge(df_gross_price, on=['product_code', 'fiscal_year']))
fy21 = merged[merged.fiscal_year == 2021].copy()
fy21['gross_sales'] = fy21['sold_quantity'] * fy21['gross_price']

by_channel = fy21.groupby('channel')['gross_sales'].sum().sort_values(ascending=False)
pct = by_channel / by_channel.sum() * 100
print(pct)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
merged = (df_sales.merge(df_customer, on='customer_code').merge(df_gross_price, on=['product_code','fiscal_year']))
fy21 = merged[merged.fiscal_year == 2021].copy()
fy21['gross_sales'] = fy21['sold_quantity'] * fy21['gross_price']
by_channel = fy21.groupby('channel')['gross_sales'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(by_channel.values, labels=by_channel.index, autopct='%1.1f%%',
       colors=['#2E5EAA','#5B9BD5','#A9CCE3'], startangle=90,
       wedgeprops={'edgecolor':'white','linewidth':2})
ax.set_title('FY2021 Gross Sales Contribution by Channel')
plt.show()
# %% [markdown]
# ### **Q.10 Identify the top 3 products in each division based on total sold quantities for the fiscal year 2021. Rank them and provide the findings.**
# %% [markdown]
# CODE:
# %%
merged = df_sales.merge(df_product, on='product_code')
fy21 = merged[merged.fiscal_year == 2021]
totals = fy21.groupby(['division','product_code','product'])['sold_quantity'].sum().reset_index()
totals['rank'] = totals.groupby('division')['sold_quantity'].rank(method='first', ascending=False)
top3 = totals[totals['rank'] <= 3].sort_values(['division','rank'])
print(top3)
# %% [markdown]
# VISUAL REPRESENTATION:
# %%
merged = df_sales.merge(df_product, on='product_code')
fy21 = merged[merged.fiscal_year == 2021]
totals = fy21.groupby(['division','product','product_code'])['sold_quantity'].sum().reset_index()
totals['rank'] = totals.groupby('division')['sold_quantity'].rank(method='first', ascending=False)
top3 = totals[totals['rank'] <= 3].sort_values(['division','rank'])

divisions = top3['division'].unique()
fig, axes = plt.subplots(1, len(divisions), figsize=(14,4))
for ax, div in zip(axes, divisions):
    sub = top3[top3.division == div].sort_values('sold_quantity')
    ax.barh(sub['product'], sub['sold_quantity'], color='#2E5EAA')
    ax.set_title(div)
plt.tight_layout()
plt.show()
# %%
