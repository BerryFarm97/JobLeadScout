import sqlite3


def init_db():
    conn = None

    try:
        conn = sqlite3.connect("job_leads.db")

        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS
            job_leads(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_job_id TEXT NOT NULL,
                job_source TEXT NOT NULL,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                url TEXT NOT NULL,
                location TEXT NOT NULL,
                salary_min REAL,
                salary_max REAL,
                salary_interval TEXT,
                job_description TEXT,
                job_location_type TEXT NOT NULL DEFAULT 'unknown',
                match_rating TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                date_found TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(job_source, source_job_id)
            )""")

        conn.commit()
        return True

    except sqlite3.Error as error:
        if conn is not None:
            conn.rollback()
        print(error)
        return False

    finally:
        if conn is not None:
            conn.close()


def get_db_connection():
    conn = sqlite3.connect("job_leads.db")
    return conn


def get_db_cursor(conn):
    return conn.cursor()
