from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "RoleFuture AI Dashboard",
        },
    )


@router.get("/roles/{role_id}")
def role_detail_page(request: Request, role_id: int):
    return templates.TemplateResponse(
        request=request,
        name="role_detail.html",
        context={
            "page_title": "Role Details",
            "role_id": role_id,
        },
    )
