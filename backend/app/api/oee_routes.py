
from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.services.oee_reporting_service import get_shift_oee_report
from app.services.daily_oee_service import get_daily_oee_report
from app.services.oee_trend_service import get_oee_trend


router = APIRouter(
    prefix="/api/v1/oee",
    tags=["OEE Analytics"]
)


@router.get("/shift/{shift_id}")
def get_shift_oee(shift_id: str):
    try:
        report = get_shift_oee_report(shift_id)

        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"No OEE data found for shift {shift_id}"
            )

        return {
            "shift_id": shift_id,
            "machine_count": len(report),
            "data": report
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate shift OEE report"
        )


@router.get("/daily/{report_date}")
def get_daily_oee(report_date: date):
    try:
        report = get_daily_oee_report(report_date.isoformat())

        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"No OEE data found for {report_date}"
            )

        return {
            "date": report_date.isoformat(),
            "machine_count": len(report),
            "data": report
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate daily OEE report"
        )


@router.get("/trend")
def get_oee_trend_api(
    start_date: date = Query(...),
    end_date: date = Query(...)
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date"
        )

    try:
        report = get_oee_trend(
            start_date.isoformat(),
            end_date.isoformat()
        )

        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days_available": len(report),
            "data": report
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate OEE trend"
        )
