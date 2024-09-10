from fastapi import APIRouter, Response
from util.auth_lib import hash, gen_token
from service.auth_service import Credential, AuthService

router = APIRouter()

@router.post("/auth/login")
def login(auth: Credential, resp: Response):
	service = AuthService()
	data = service.read(auth.username)

	hashed = hash(auth.password, data.salt)
	if data.username != auth.username or data.password != hashed:
		resp.status_code = 401
		return {
			"ok": 0,
			"errno": "Unauthorized"
		}
	
	token = gen_token(auth.username, hashed)
	return {
		"ok": 1,
		"token": "Basic {}".format(token)
	}
