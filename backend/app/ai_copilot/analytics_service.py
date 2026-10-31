
from sqlalchemy import text

from app.database.connection import engine
from app.services.daily_oee_service import get_daily_oee_report
from app.services.oee_reporting_service import get_shift_oee_report
from app.services.line_oee_service import get_line_oee_report


def get_latest_date():
    """Get the latest available manufacturing date."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT MAX(shift_date) FROM shifts")
        ).scalar()

    return result


def get_line_machine_mapping():
    """Retrieve production lines and their associated machines."""
    with engine.connect() as connection:
        rows = connection.execute(
            text("""
                SELECT
                    pl.line_id,
                    pl.line_name,
                    m.machine_id,
                    m.machine_name
                FROM production_lines pl
                JOIN machines m ON pl.line_id = m.line_id
                ORDER BY pl.line_id, m.machine_id
            """)
        ).mappings().all()

    return [dict(row) for row in rows]


def get_analytics_context(question: str) -> dict:
    """
    Route manufacturing questions to existing analytics services.
    Returns actual database-backed metrics for the RAG Copilot.
    """

    question_lower = question.lower()

    context = {
        "analytics_available": True,
        "question": question,
    }

    try:
        latest_date = get_latest_date()

        if not latest_date:
            return {
                **context,
                "analytics_error": "No manufacturing data is available."
            }

        # Machine and daily OEE analytics
        if any(word in question_lower for word in [
            "machine", "oee", "availability",
            "performance", "quality", "downtime"
        ]):
            report_date = latest_date

            if "yesterday" in question_lower:
                from datetime import timedelta
                report_date -= timedelta(days=1)

            daily_report = get_daily_oee_report(
                report_date.isoformat()
            )

            context["report_date"] = report_date.isoformat()
            context["daily_oee"] = daily_report

            if daily_report:
                context["lowest_oee_machine"] = min(
                    daily_report,
                    key=lambda x: x["oee"]
                )

                context["highest_oee_machine"] = max(
                    daily_report,
                    key=lambda x: x["oee"]
                )

                context["highest_downtime_machine"] = max(
                    daily_report,
                    key=lambda x: x.get("downtime_sec", 0)
                )

        # Production-line analytics
        if "line" in question_lower:
            with engine.connect() as connection:
                shift = connection.execute(
                    text("""
                        SELECT shift_id, shift_code, shift_date
                        FROM shifts
                        ORDER BY shift_date DESC, start_time DESC
                        LIMIT 1
                    """)
                ).mappings().first()

            if shift:
                line_report = get_line_oee_report(
                    shift["shift_id"]
                )

                context["line_oee"] = line_report
                context["selected_shift"] = dict(shift)

                if line_report:
                    context["best_performing_line"] = max(
                        line_report,
                        key=lambda x: x["oee"]
                    )

                    context["lowest_performing_line"] = min(
                        line_report,
                        key=lambda x: x["oee"]
                    )

        # Shift analytics
        if "shift" in question_lower:
            with engine.connect() as connection:
                shift = connection.execute(
                    text("""
                        SELECT shift_id, shift_code, shift_date
                        FROM shifts
                        ORDER BY shift_date DESC, start_time DESC
                        LIMIT 1
                    """)
                ).mappings().first()

            if shift:
                context["shift_oee"] = get_shift_oee_report(
                    shift["shift_id"]
                )
                context["selected_shift"] = dict(shift)

        # Machine-to-line mapping
        if any(word in question_lower for word in [
            "line", "machine"
        ]):
            context["line_machine_mapping"] = (
                get_line_machine_mapping()
            )

    except Exception as error:
        context["analytics_available"] = False
        context["analytics_error"] = str(error)
def get_anomaly_context():
    """
    Retrieve existing anomaly detection results
    and data-quality findings from the database.
    """
    from app.services.anomaly_detection_service import (
        get_anomaly_summary
    )

    return get_anomaly_summary()
    return context

