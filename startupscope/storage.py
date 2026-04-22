import sqlite3
import json
from typing import List, Optional
from startupscope.config import Config
from startupscope.models import ValidationReport
from startupscope.logger import logger
from startupscope.exceptions import DatabaseConnectionError

def _get_connection():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise DatabaseConnectionError("Could not connect to SQLite database.")

def init_db():
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id TEXT NOT NULL,
                version_id INTEGER NOT NULL,
                startup_name TEXT NOT NULL,
                industry TEXT NOT NULL,
                business_type TEXT NOT NULL,
                overall_score INTEGER NOT NULL,
                generated_at TEXT NOT NULL,
                report_json TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except DatabaseConnectionError:
        pass

def save_report(report: ValidationReport):
    init_db()
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # Determine the next version ID for this startup name
        cursor.execute('''
            SELECT MAX(version_id) as max_version
            FROM reports
            WHERE startup_name = ?
        ''', (report.input_data.name,))
        row = cursor.fetchone()
        
        next_version = 1
        if row and row['max_version'] is not None:
            next_version = row['max_version'] + 1
            
        report.version_id = next_version
        
        cursor.execute('''
            INSERT INTO reports (report_id, version_id, startup_name, industry, business_type, overall_score, generated_at, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report.report_id,
            report.version_id,
            report.input_data.name,
            report.input_data.industry,
            report.input_data.business_type,
            report.scores.overall_score,
            report.generated_at,
            report.model_dump_json()
        ))
        conn.commit()
        conn.close()
        logger.info(f"Saved report {report.report_id} version {report.version_id} to database.")
    except Exception as e:
        logger.error(f"Failed to save report: {e}")

def get_all_reports() -> List[ValidationReport]:
    init_db()
    reports = []
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT report_json FROM reports ORDER BY generated_at DESC')
        rows = cursor.fetchall()
        
        for row in rows:
            data = json.loads(row['report_json'])
            reports.append(ValidationReport(**data))
        conn.close()
    except Exception as e:
        logger.error(f"Failed to fetch reports: {e}")
    return reports

def delete_report(report_id: str):
    init_db()
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reports WHERE report_id = ?', (report_id,))
        conn.commit()
        conn.close()
        logger.info(f"Deleted report {report_id}.")
    except Exception as e:
        logger.error(f"Failed to delete report: {e}")
