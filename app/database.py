import sqlite3


def get_db_connection(db_path="job_leads.db"):
    return sqlite3.connect(db_path)


def get_db_cursor(conn):
    return conn.cursor()


def init_db(db_path="job_leads.db"):
    conn = None

    try:
        conn = get_db_connection(db_path)

        cur = get_db_cursor(conn)

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


def add_job_lead(
    source_job_id,
    job_source,
    company_name,
    job_title,
    url,
    location,
    db_path="job_leads.db",
):
    conn = None

    try:
        conn = get_db_connection(db_path)
        cur = get_db_cursor(conn)

        cur.execute(
            """INSERT INTO job_leads
            (source_job_id, job_source, company_name, job_title, url, location)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                source_job_id,
                job_source,
                company_name,
                job_title,
                url,
                location,
            ),
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        if conn is not None:
            conn.rollback()
        return False

    except sqlite3.Error as error:
        if conn is not None:
            conn.rollback()
        print(error)
        return False

    finally:
        if conn is not None:
            conn.close()


def get_all_job_leads(db_path="job_leads.db"):
    conn = None
    try:
        conn = get_db_connection(db_path)
        conn.row_factory = sqlite3.Row

        cur = get_db_cursor(conn)

        cur.execute("""SELECT * FROM job_leads
            ORDER BY date_found DESC, id DESC""")

        rows = cur.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as error:
        print(error)
        return None

    finally:
        if conn is not None:
            conn.close()
