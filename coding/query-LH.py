import pyodbc
from msal import ConfidentialClientApplication

# === Configuration ===
sql_endpoint = "your-lakehouse.sql.azuresynapse.net"
database = "YourLakehouseName"
client_id = "your-client-id"
tenant_id = "your-tenant-id"
client_secret = "your-client-secret"
sql_query = "SELECT TOP 10 * FROM YourTable"

# === Get Azure AD Access Token ===
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://sql.azuresynapse.net/.default"]

app = ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)

token_response = app.acquire_token_for_client(scopes=scope)

if "access_token" not in token_response:
    raise Exception(f"Authentication failed: {token_response.get('error_description')}")

access_token = token_response["access_token"]

# === Connect to Fabric Lakehouse via ODBC ===
conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{sql_endpoint},1433;"
    f"Database={database};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Authentication=ActiveDirectoryAccessToken"
)

# === Run SQL Query ===
with pyodbc.connect(conn_str, attrs_before={1256: access_token}) as conn:
    cursor = conn.cursor()
    cursor.execute(sql_query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    for row in rows:
        row_dict = dict(zip(columns, row))
        print(row_dict)
