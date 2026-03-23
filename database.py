import sqlite3
import logging
from datetime import datetime, timedelta
from config import DB_PATH

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            first_name  TEXT,
            joined_at   TEXT DEFAULT (datetime('now')),
            is_banned   INTEGER DEFAULT 0,
            is_premium  INTEGER DEFAULT 0,
            keys_today  INTEGER DEFAULT 0,
            last_key_date TEXT,
            total_keys  INTEGER DEFAULT 0,
            referrals   INTEGER DEFAULT 0,
            ref_by      INTEGER DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS keys (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            server_name TEXT,
            server_url  TEXT,
            key_value   TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            expires_at  TEXT,
            is_active   INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS stats (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            total_users INTEGER DEFAULT 0,
            total_keys  INTEGER DEFAULT 0,
            updated_at  TEXT DEFAULT (datetime('now'))
        );
    """)
    
    conn.commit()
    conn.close()
    logging.info("✅ База данных инициализирована")

def register_user(user_id: int, username: str, first_name: str, ref_by: int = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name, ref_by)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, first_name, ref_by))
    
    if ref_by and cur.rowcount > 0:
        cur.execute("""
            UPDATE users SET referrals = referrals + 1
            WHERE user_id = ?
        """, (ref_by,))
    
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

def can_get_key(user_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT keys_today, last_key_date, is_premium 
        FROM users WHERE user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return False
    
    keys_today, last_key_date, is_premium = row
    today = datetime.now().strftime("%Y-%m-%d")
    
    if is_premium:
        return True
    
    if last_key_date != today:
        return True
    
    return keys_today < 1

def save_key(user_id: int, server_name: str, server_url: str, key_value: str):
    conn = get_conn()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    expires = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    cur.execute("""
        INSERT INTO keys (user_id, server_name, server_url, key_value, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, server_name, server_url, key_value, expires))
    
    cur.execute("""
        UPDATE users 
        SET keys_today = CASE WHEN last_key_date = ? THEN keys_today + 1 ELSE 1 END,
            last_key_date = ?,
            total_keys = total_keys + 1
        WHERE user_id = ?
    """, (today, today, user_id))
    
    conn.commit()
    conn.close()

def get_user_keys(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT server_name, key_value, created_at, expires_at, is_active
        FROM keys WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 10
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM keys")
    total_keys = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE is_premium = 1")
    premium_users = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM users 
        WHERE joined_at >= datetime('now', '-1 day')
    """)
    new_today = cur.fetchone()[0]
    conn.close()
    return total_users, total_keys, premium_users, new_today

def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE is_banned = 0")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def ban_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def set_premium(user_id: int, status: bool = True):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_premium = ? WHERE user_id = ?", 
                (1 if status else 0, user_id))
    conn.commit()
    conn.close()