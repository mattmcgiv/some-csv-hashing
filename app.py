import hashlib
import random
import pandas as pd

# Use Case 1: 12-digit numerical hash
def hash_account_id(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    # Convert to int, then truncate to 12 digits
    return str(int(m.hexdigest(), 16))[:12]

# Use Case 2: 10-digit numerical hash
def hash_aws_invoice(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    return str(int(m.hexdigest(), 16))[:10]

# Use Case 3: 8-digit numerical hash or 'N/A'
def hash_high_side_invoice(value):
    if value == "N/A":
        return "N/A"
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    return str(int(m.hexdigest(), 16))[:8]

# Use Case 4: Random integer between -100,000 and 10,000,000
def randomize_invoice_amount(value):
    return random.randint(-100000, 10000000)

# Use Case 5: Hash the values in the Contract, Task Order, and CLIN columns
def hash_contract(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    output = str(int(m.hexdigest(), 16))[:4]
    if random.random() < 0.5:
        output += str(random.randint(0, 9))
    return output

def hash_task_order(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    output = str(int(m.hexdigest(), 16))[:4]
    if len(output) == 3:
        output += str(random.randint(0, 9))
    return output

def hash_clin(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    output = str(int(m.hexdigest(), 16))[:4]
    output = ''.join(filter(str.isdigit, output))
    if len(output) < 4:
        output += str(random.randint(0, 9))
    return output

# Use Case 6: Hash the value in the "Agency" column
def hash_agency(value):
    m = hashlib.sha256()
    m.update(str(value).encode('utf-8'))
    return m.hexdigest()

# Read CSV file into a DataFrame
df = pd.read_csv('input.csv')

# Apply the hashing and randomization functions to the respective columns
df['Account ID'] = df['Account ID'].apply(hash_account_id)
df['AWS Invoice #'] = df['AWS Invoice #'].apply(hash_aws_invoice)
df['High-side Invoice #'] = df['High-side Invoice #'].apply(hash_high_side_invoice)
df['Invoice Amount'] = df['Invoice Amount'].apply(randomize_invoice_amount)
df['Contract'] = df['Contract'].apply(hash_contract)
df['Task Order'] = df['Task Order'].apply(hash_task_order)
df['CLIN'] = df['CLIN'].apply(hash_clin)
df['Agency'] = df['Agency'].apply(hash_agency)

# Save the DataFrame back to a new CSV file
df.to_csv('hashed.csv', index=False)