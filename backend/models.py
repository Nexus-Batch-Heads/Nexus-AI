"""
NEXUS — MSSQL User Model
Handles DB connection, user table creation, and CRUD using pyodbc.
"""
import pyodbc
import bcrypt
from datetime import datetime
from flask_login import UserMixin
from config import MSSQL_CONNECTION_STRING


def get_db():
    """Return a new MSSQL connection."""
    return pyodbc.connect(MSSQL_CONNECTION_STRING)


def init_db():
    """Create the users table if it doesn't exist."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects WHERE name='users' AND xtype='U'
        )
        CREATE TABLE users (
            id            INT IDENTITY(1,1) PRIMARY KEY,
            name          NVARCHAR(120)  NOT NULL,
            email         NVARCHAR(255)  NOT NULL UNIQUE,
            password_hash NVARCHAR(255)  NOT NULL,
            created_at    DATETIME       DEFAULT GETDATE()
        )
    """)
    conn.commit()
    conn.close()
    print("  [DB] Users table ready.")


class User(UserMixin):
    """Flask-Login compatible User object."""

    def __init__(self, id, name, email, created_at=None):
        self.id         = id
        self.name       = name
        self.email      = email
        self.created_at = created_at

    # ---- Class methods (DB queries) ----

    @classmethod
    def get_by_id(cls, user_id: int):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_by_email(cls, email: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, created_at FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    @classmethod
    def create(cls, name: str, email: str, password: str):
        """Hash the password and insert a new user. Returns the User or None on duplicate."""
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, pw_hash)
            )
            conn.commit()
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            conn.close()
            return cls(*row) if row else None
        except pyodbc.IntegrityError:
            conn.close()
            return None  # email already exists

    @classmethod
    def verify_password(cls, email: str, password: str):
        """Return User if password matches, else None."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, created_at, password_hash FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        uid, name, em, created_at, pw_hash = row
        if bcrypt.checkpw(password.encode(), pw_hash.encode()):
            return cls(uid, name, em, created_at)
        return None
