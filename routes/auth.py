from fastapi import APIRouter
from service.auth_service import Credential

router = APIRouter()

@router.post("/auth/login")
def login(auth: Credential):
	return {"ok": 1, "token": "Basic {}"}
