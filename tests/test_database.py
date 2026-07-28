import sqlite3
from app.database import init_db


def test_init_db_creates_database_file(tmp_path):
    test_db = tmp_path / "test_job_leads.db"
    result = init_db(test_db)

    assert result is True
    assert test_db.exists()


def test_init_db_creates_job_leads_table(tmp_path):
    test_db = tmp_path / "test_job_leads_table.db"
    init_db(test_db)

    test_conn = sqlite3.connect(test_db)
    test_cur = test_conn.cursor()

    query = """SELECT name
    FROM sqlite_master
    WHERE type = 'table' AND name = ?"""

    test_cur.execute(query, ("job_leads",))
    table = test_cur.fetchone()
    test_conn.close()

    assert table == ("job_leads",)
