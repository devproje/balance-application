from datetime import datetime
from fastapi import APIRouter, Response, Request
from service.auth_service import AuthService
from service.balance_service import Balance, BalanceService, UpdateForm

router = APIRouter()

@router.post("/balance", status_code=201)
def insert(balance: Balance, req: Request, resp: Response):
	started = datetime.now().microsecond / 1000
	auth = AuthService()

	if not auth.check_auth(req):
		resp.status_code = 403
		return {
			"ok": 0,
			"errno": "permission denied"
		}
	
	info = auth.get_data(req)

	service = BalanceService()
	ok = service.create(info["username"], balance=balance)
	if not ok == 1:
		resp.status_code = 500
		return {
			"ok": 0,
			"errno": "error occurred to running transaction"
		}

	return {
		"ok": 1,
		"name": balance.name,
		"is_buy": balance.buy,
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.get("/balance")
def query(req: Request, resp: Response):
	started = datetime.now().microsecond / 1000
	auth = AuthService()
	if not auth.check_auth(req):
		resp.status_code = 403
		return {
			"ok": 0,
			"errno": "permission denied"
		}
	
	service = BalanceService()
	data = service.query()
	if data == None:
		resp.status_code = 204
		return {
			"ok": 0,
			"errno": "no content"
		}
	
	return {
		"ok": 1,
		"data": data,
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.get("/balance/{id}")
def find(id, req: Request, resp: Response):
	started = datetime.now().microsecond / 1000
	auth = AuthService()

	if not auth.check_auth(req):
		resp.status_code = 403
		return {
			"ok": 0,
			"errno": "permission denied"
		}

	service = BalanceService()
	data = service.read(int(id))
	
	if data == None:
		resp.status_code = 204
		return {"ok": 0, "errno": "id '{}' result is not found".format(id)}

	return {
		"ok": 1,
		"id": int(id),
		"data": data,
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.put("/balance/{id}")
def update(id, balance: UpdateForm, req: Request, resp: Response):
	started = datetime.now().microsecond / 1000
	auth = AuthService()

	print(auth.check_auth(req))
	if not auth.check_auth(req):
		resp.status_code = 403
		return {
			"ok": 0,
			"errno": "permission denied"
		}
	
	service = BalanceService()

	ok = service.update(
		int(id),
		UpdateForm(balance.name, balance.date, balance.price, balance.buy, balance.memo)
	)

	if not ok == 1:
		resp.status_code = 500
		return {
			"ok": 0,
			"errno": "error occurred to running transaction"
		}

	return {
		"ok": 1,
		"id": int(id),
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.delete("/balance/{id}")
def delete(id, req: Request, resp: Response):
	started = datetime.now().microsecond / 1000
	auth = AuthService()

	if not auth.check_auth(req):
		resp.status_code = 403
		return {
			"ok": 0,
			"errno": "permission denied"
		}

	service = BalanceService()
	ok = service.delete(int(id))
	if not ok == 1:
		resp.status_code = 500
		return {
			"ok": 0,
			"errno": "error occurred to running transaction"
		}

	return {
		"ok": 1,
		"id": int(id),
		"respond_time": "{}ms".format((round(datetime.now().microsecond / 1000) - started))
	}
