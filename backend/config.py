import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY        = os.getenv("GEMINI_API_KEY", "")
FLASK_PORT            = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG           = os.getenv("FLASK_DEBUG", "true").lower() == "true"
SECRET_KEY            = os.getenv("SECRET_KEY", "nexus-super-secret-key-change-in-prod")
MSSQL_CONNECTION_STRING = os.getenv(
    "MSSQL_CONNECTION_STRING",
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=nexus;Trusted_Connection=yes;TrustServerCertificate=yes;"
)
