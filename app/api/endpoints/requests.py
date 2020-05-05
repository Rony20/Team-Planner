from fastapi import APIRouter, Query
from ...crud.requests import(
    make_new_request,
    get_requests_by_pm,
    get_all_requests,
    approve_reject_request_by_pmo,
    check_for_conflicts
)

from ...models.requests import (
    Request,
    UpdateRequestByPMO,
    UpdateRequestByPM
)

from ...crud.projects import get_projects_with_remaining_requests

router = APIRouter()
date_regex = r"(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-]\d{4}"


@router.post("/make-new-request")
def make_new_request_api(request: Request) -> bool:
    return make_new_request(request)


@router.get("/get-all-requests")
def get_all_requests_api() -> list:
    return get_all_requests()


@router.get("/get-all-requests-by-pm/{pm_id}")
def get_requests_by_pm_api(pm_id: int, week_start: str = Query(..., regex=date_regex), week_end: str = Query(..., regex=date_regex)):
    return get_requests_by_pm(pm_id, week_start, week_end)


@router.patch("/change-request-status/{request_id}")
def approve_reject_request_by_pmo_api(request_id: str, updateRequest: UpdateRequestByPMO):
    return approve_reject_request_by_pmo(request_id, updateRequest)

@router.get("/get-projects-with-remaining-requests-by-pm/{pm_id}")
def get_projects_with_remaining_requests_api(pm_id: int):
    return get_projects_with_remaining_requests(pm_id)


@router.get("/check-conflicts/{employee_id}")
def get_conflict_status_for_employee_api(employee_id: int):
    return check_for_conflicts(employee_id)