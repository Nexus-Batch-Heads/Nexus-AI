"""
NEXUS — SQLite User Model with Conversation History
Handles DB connection, user table, conversation history, and simulation history.
"""
import sqlite3
import bcrypt
from datetime import datetime
from flask_login import UserMixin
from pathlib import Path

DB_PATH = Path(__file__).parent / "nexus.db"


def get_db():
    """Return a new SQLite connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Conversation history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            message    TEXT NOT NULL,
            response   TEXT NOT NULL,
            confidence INTEGER,
            latency_ms INTEGER,
            source     TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Simulation history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id           INTEGER NOT NULL,
            scenario          TEXT NOT NULL,
            experience        INTEGER,
            risk_tolerance    INTEGER,
            financial_runway  INTEGER,
            path_a_prob       INTEGER,
            path_b_prob       INTEGER,
            recommendation    TEXT,
            created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # User preferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id           INTEGER PRIMARY KEY,
            communication_style TEXT DEFAULT 'professional',
            response_length   TEXT DEFAULT 'concise',
            formality_level   INTEGER DEFAULT 5,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    print("  [DB] SQLite database initialized.")


class User(UserMixin):
    """Flask-Login compatible User object."""

    def __init__(self, id, name, email, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at

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
            return cls(row['id'], row['name'], row['email'], row['created_at'])
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
            return cls(row['id'], row['name'], row['email'], row['created_at'])
        return None

    @classmethod
    def create(cls, name: str, email: str, password: str):
        """Hash the password and insert a new user."""
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, pw_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            # Create default preferences
            cursor.execute(
                "INSERT INTO user_preferences (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            conn.close()
            return cls(row['id'], row['name'], row['email'], row['created_at']) if row else None
        except sqlite3.IntegrityError:
            conn.close()
            return None

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
        if bcrypt.checkpw(password.encode(), row['password_hash'].encode()):
            return cls(row['id'], row['name'], row['email'], row['created_at'])
        return None


class Conversation:
    """Conversation history management."""
    
    @staticmethod
    def save(user_id: int, message: str, response: str, confidence: int, latency_ms: int, source: str):
        """Save a conversation to history."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO conversations 
               (user_id, message, response, confidence, latency_ms, source) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, message, response, confidence, latency_ms, source)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_history(user_id: int, limit: int = 50):
        """Get conversation history for a user."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT message, response, confidence, latency_ms, source, created_at 
               FROM conversations 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT ?""",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


class Simulation:
    """Simulation history management."""
    
    @staticmethod
    def save(user_id: int, scenario: str, params: dict, path_a_prob: int, path_b_prob: int, recommendation: str):
        """Save a simulation to history."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO simulations 
               (user_id, scenario, experience, risk_tolerance, financial_runway, 
                path_a_prob, path_b_prob, recommendation) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, scenario, params.get('experience'), params.get('risk_tolerance'),
             params.get('financial_runway'), path_a_prob, path_b_prob, recommendation)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_history(user_id: int, limit: int = 20):
        """Get simulation history for a user."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT scenario, experience, risk_tolerance, financial_runway,
                      path_a_prob, path_b_prob, recommendation, created_at 
               FROM simulations 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT ?""",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
