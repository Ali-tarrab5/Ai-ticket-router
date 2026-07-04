import pandas as pd
import random

# 1. Departments and their common keywords/phrases
categories = {
    'Billing': ['overcharged', 'invoice', 'credit card declined', 'payment failed', 'billing cycle', 'update payment method', 'charged twice'],
    'Technical Support': ['app keeps crashing', 'cannot login', 'forgot password', 'error 404', 'screen frozen', 'bug in software', 'slow performance'],
    'Refunds': ['want my money back', 'cancel my subscription', 'return product', 'not satisfied', 'refund policy', 'process my refund'],
    'General Inquiry': ['business hours', 'where is your office', 'talk to human', 'international shipping', 'pricing plans', 'contact number']
}

data = []

# 2. Generate 1000 random customer tickets
for _ in range(1000):
    category = random.choice(list(categories.keys()))
    
    # Mix words to create fake sentences
    phrase1 = random.choice(categories[category])
    phrase2 = random.choice(categories[category])
    
    # Adding some noise (common words people use)
    intros = ["Hi, ", "Hello, ", "Please help, ", "I am writing because ", "Urgent: ", ""]
    outros = [". Please fix this.", ". Thanks.", ". Need help ASAP.", ". Regards.", ""]
    
    ticket_text = f"{random.choice(intros)}{phrase1} and {phrase2}{random.choice(outros)}"
    
    data.append({'ticket_text': ticket_text, 'department': category})

# 3. Save to CSV
df = pd.DataFrame(data)
# Shuffle the dataset
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv('customer_tickets.csv', index=False)

print("✅ 'customer_tickets.csv' successfully created with 1000 rows!")