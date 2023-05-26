"""
Functions for interacting with the database.

The database hosts a single table: `entitlement`, which we use to persist
all the entitlements for every app customer.

We're using sqlite for simplicity and ease to get setup and running locally.
However, the idea is that these high-level functions can be easily swapped to use
your database of choice.
"""
from sqlite3 import Connection


def db_create_ent_table(db_conn: Connection):
    """Idempotent function to create the entitlements table if it doesn't exist"""
    sql = """
    CREATE TABLE IF NOT EXISTS entitlement(
        user_id TEXT,
        entitlement TEXT,
        expiration NUM,
        last_sync NUM,
        source TEXT);
    """
    db_conn.execute(sql)
    db_conn.commit()


def db_fetch_entitlements(db_conn: Connection, user_id: str):
    """Fetch all entitlements for a given user

    We fetch by user rather than entitlements because we might see new entitlements
    """
    result = db_conn.execute('SELECT * FROM entitlement WHERE user_id=:user_id', {'user_id': user_id})
    return result.fetchall()


def db_insert_entitlement(db_conn: Connection, row: dict) -> int:
    """
    Insert a new entitlement for a user.

    Should only be called once you've fetched their entitlements to ensure this is new,
    otherwise you should update the existing entitlement(s)
    """
    result = db_conn.execute(
        'INSERT INTO entitlement VALUES (:user_id, :entitlement, :expiration, :last_sync, :source)',
        row)
    db_conn.commit()
    return result.rowcount


def db_update_entitlement(db_conn: Connection, row: dict) -> int:
    """Update a user's existing entitlement. Overwrites the whole row"""
    result = db_conn.execute('UPDATE entitlement WHERE user_id=:user_id AND entitlement=:entitlement'
                             'VALUES (:user_id, :entitlement, :expiration, :last_sync, :source)',
                             row)
    db_conn.commit()
    return result.rowcount


def db_dict_factory(cursor, row) -> dict:
    """
    Returns rows as dictionaries with column name as keys.

    This is a python/sqlite3 specific function because we're not using
    an ORM for this simple sample app. You can safely ignore it for your purposes.
    """
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}
