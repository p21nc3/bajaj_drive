import pandas as pd
from sqlalchemy import create_engine, text

# Establish a connection to MySQL
engine = create_engine('mysql+mysqlconnector://prince:helloworld@localhost/bajajtest')

# Function to create MySQL table
def create_table(table_name, schema):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"))

# Function to load data into MySQL table
def load_data(table_name, file_path):
    df = pd.read_parquet(file_path)
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

# Define the schemas for each table
claim_schema = '''ClaimId INT, CustomerId INT, PolicyId VARCHAR(255), ProductId VARCHAR(255),
                  ClaimDate VARCHAR(255), ClaimApprovedDate VARCHAR(255), ClaimStatus VARCHAR(255),
                  ClaimSource VARCHAR(255), ClaimAmount INT'''

policy_schema = '''CustomerId INT, PolicyId VARCHAR(255), ProductId VARCHAR(255),
                   PurchaseDate VARCHAR(255), ExpiryDate VARCHAR(255), CancellationDate VARCHAR(255),
                   Status VARCHAR(255), Premium INT, MembersCovered INT'''

product_schema = '''ProductId VARCHAR(255), ProductName VARCHAR(255), ProductGroup VARCHAR(255)'''

# Create tables and load data
create_table('claim', claim_schema)
load_data('claim', 'claim.parquet')

create_table('policy', policy_schema)
load_data('policy', 'policy.parquet')

create_table('product', product_schema)
load_data('product', 'product.parquet')

# SQL query to fetch data metrics
query = '''
SELECT
    (
        SELECT ProductGroup
        FROM product
        GROUP BY ProductGroup
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS HighestSaleProductGroup,
    (
        SELECT ProductGroup
        FROM product p
        INNER JOIN policy po ON p.ProductId = po.ProductId
        INNER JOIN claim c ON po.PolicyId = c.PolicyId
        WHERE YEAR(c.ClaimDate) = 2022
        GROUP BY ProductGroup
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS ProductGroupWithHighestClaims2022,
    (
        SELECT SUM(Premium)
        FROM policy
        WHERE YEAR(PurchaseDate) = 2022
    ) AS TotalRevenuePremium2022,
    (
        SELECT COUNT(DISTINCT ProductGroup)
        FROM product p
        INNER JOIN policy po ON p.ProductId = po.ProductId
        INNER JOIN claim c ON po.PolicyId = c.PolicyId
    ) AS ProductGroupsWithClaimsRegistered,
    (
        SELECT COUNT(DISTINCT po.PolicyId)
        FROM policy po
        INNER JOIN claim c ON po.PolicyId = c.PolicyId
        WHERE MONTH(c.ClaimApprovedDate) = 1 AND YEAR(c.ClaimApprovedDate) = 2023
    ) AS PoliciesWithClaimsJan2023,
    (
        SELECT COUNT(DISTINCT CustomerId)
        FROM claim
    ) AS UniqueCustomersWithClaims,
    (
        SELECT COUNT(DISTINCT po.PolicyId)
        FROM policy po
        LEFT JOIN claim c ON po.PolicyId = c.PolicyId
        WHERE c.ClaimId IS NULL
    ) AS PoliciesWithoutClaims,
    (
        SELECT COUNT(DISTINCT p.ProductId)
        FROM policy p
        LEFT JOIN claim c ON p.PolicyId = c.PolicyId
        WHERE c.ClaimId IS NULL AND p.Status = 'Active'
    ) AS UniqueProductsActivePoliciesNoClaims,
    (
        SELECT COUNT(DISTINCT po.PolicyId)
        FROM policy po
        INNER JOIN claim c ON po.PolicyId = c.PolicyId
        WHERE c.ClaimDate > po.ExpiryDate
    ) AS UniquePoliciesClaimAfterExpiration,
    (
        SELECT COUNT(DISTINCT po.PolicyId)
        FROM policy po
        INNER JOIN claim c ON po.PolicyId = c.PolicyId
        WHERE c.ClaimAmount >= po.Premium
    ) AS PoliciesWithClaimAmountMoreThanPremium
'''

# Execute the SQL query and fetch the results
with engine.connect() as conn:
    result = conn.execute(text(query))
    row = result.fetchone()
    data_metrics = '-'.join(str(value) for value in row)

# Print the data metrics
print(f"Data Metrics: {data_metrics}")
