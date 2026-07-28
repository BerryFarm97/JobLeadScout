import sqlite3
from app.database import init_db, add_job_lead, get_all_job_leads


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


def test_add_job_lead_inserts_valid_job(tmp_path):
    test_job_details = (
        "Zk9mP2nQ4R",
        "LinkedIn",
        "Amazon",
        "Python Backend Developer ENTRY",
        "https://www.amazon.com/careers",
        "USA",
    )

    test_db = tmp_path / "test_job_leads_table.db"
    init_db(test_db)

    result = add_job_lead(*test_job_details, db_path=test_db)
    assert result is True

    test_conn = sqlite3.connect(test_db)
    test_cur = test_conn.cursor()

    query = """SELECT
    source_job_id,
    job_source,
    company_name,
    job_title,
    url,
    location
    FROM job_leads WHERE source_job_id = ?"""

    test_cur.execute(query, (test_job_details[0],))
    row = test_cur.fetchone()
    test_conn.close()

    assert row == test_job_details


def test_add_job_lead_rejects_duplicate_source_job(tmp_path):
    test_job_details = (
        "Zk9mP2nQ4U",
        "LinkedIn",
        "Amazon",
        "Python Backend Developer ENTRY",
        "https://www.amazon.com/careers",
        "USA",
    )

    test_db = tmp_path / "test_job_leads_table.db"
    init_db(test_db)

    first_result = add_job_lead(*test_job_details, db_path=test_db)
    assert first_result is True

    duplicate_result = add_job_lead(*test_job_details, db_path=test_db)
    assert duplicate_result is False

    test_conn = sqlite3.connect(test_db)
    test_cur = test_conn.cursor()

    query = "SELECT COUNT(*) FROM job_leads"

    test_cur.execute(query)
    job_count = test_cur.fetchone()[0]

    test_conn.close()

    assert job_count == 1


def test_get_all_job_leads_returns_empty_list(tmp_path):
    test_db = tmp_path / "test_job_leads_table.db"
    init_db(test_db)

    empty_result = get_all_job_leads(db_path=test_db)

    assert empty_result == []


def test_get_all_job_leads_returns_stored_job_as_dictionary(tmp_path):
    test_job_details = (
        "Zk9mP2nQ4$",
        "LinkedIn",
        "Amazon",
        "Python Backend Developer ENTRY",
        "https://www.amazon.com/careers",
        "USA",
    )
    test_db = tmp_path / "test_job_leads_table.db"
    init_db(test_db)
    add_job_lead(*test_job_details, db_path=test_db)

    test_result = get_all_job_leads(db_path=test_db)

    assert isinstance(test_result, list) is True
    assert len(test_result) == 1

    stored_job = test_result[0]
    assert isinstance(stored_job, dict)

    assert stored_job["source_job_id"] == test_job_details[0]
    assert stored_job["job_source"] == test_job_details[1]
    assert stored_job["company_name"] == test_job_details[2]
    assert stored_job["job_title"] == test_job_details[3]
    assert stored_job["url"] == test_job_details[4]
    assert stored_job["location"] == test_job_details[5]

    assert stored_job["status"] == "new"
    assert stored_job["job_location_type"] == "unknown"
