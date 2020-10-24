import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
s1 = pd.read_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh sales statistics\venus dsh data analysis\Final_venusdsh_customers_invoice datasheet\customer_95.xlsx')
s2 = pd.read_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh sales statistics\venus dsh data analysis\Final_venusdsh_customers_invoice datasheet\customer_96.xlsx')
s3 = pd.read_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh sales statistics\venus dsh data analysis\Final_venusdsh_customers_invoice datasheet\customer_97.xlsx')
s4 = pd.read_excel(r'C:\Users\meysam-sadat\Desktop\venus dsh sales statistics\venus dsh data analysis\Final_venusdsh_customers_invoice datasheet\customer_98.xlsx')
df = pd.concat([s1,s2,s3,s4],ignore_index=True)
df.sort_values('date',ascending=True,inplace=True)
df.to_excel(r'C:\Users\meysam-sadat\Desktop\venusdshconcat.xlsx')
# the way you Enode repated items:
# customer_mapping = {label:idx for idx,label in enumerate(np.unique(df['customer_name']))}
# df['customer_name'] = df['customer_name'].map(customer_mapping)
# code_customers = df.customer_name.value_counts()

# description_mapping = {label:idx for idx,label in enumerate(np.unique(df['description']))}
# df['description'] = df['description'].map(description_mapping)
# description_unique = df.description.value_counts()

# df['description'] = df['description'].str.strip()
df_customer_name = df.customer_name.value_counts()
df = df[df['description'].str.contains('مته')]
df = df.loc[df['customer_name'].isin(['ميرزايي رضا(تهران )','سلطان ميراحمد(تهران ) ويزيتور','ميرزايي (شهرستان ) حق الزحمه'])]
basket = df.groupby(['date','description'])['qty'].sum().unstack().reset_index().fillna(0).set_index('date')

basket.info()
def encode_unit(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
basket_sets = basket.applymap(encode_unit)
frequent_items = apriori(basket_sets, min_support=0.10, use_colnames=True)
rules = association_rules(frequent_items, metric='lift',min_threshold=1)

# rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
# rules = rules[rules['antecedents'] == {'مته چهارشيار8X16'}]
# rules = rules[(rules.lift > 1.5)]

rules['support'].max()
rules = rules[(rules.confidence > 0.8)&(rules.lift >= 2.0)&(rules.support >= 0.2)]





