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

@router.patch("/balance/{action}/{id}")
def update(action, id, balance: UpdateForm, req: Request, resp: Response):
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
	if action != "name" and action != "date" and action != "price" and action != "buy" and action != "memo":
		print(action)
		print(id)
		resp.status_code = 400
		return {"ok": 0, "errno": "action must be to name, date, price or memo"}
	
	if action == "name" and balance.name == "":
		resp.status_code = 400
		return {"ok": 0, "action": action, "errno": "name value cannot be empty"}
	
	if action == "date" and balance.date <= 0:
		resp.status_code = 400
		return {"ok": 0, "action": action, "errno": "date value cannot be 0 or minus"}
	
	if action == "price" and balance.price <= 0:
		resp.status_code = 400
		return {"ok": 0, "action": action, "errno": "price value cannot be 0 or minus"}
	
	if action == "memo" and len(balance.memo) > 300:
		resp.status_code = 400
		return {
			"ok": 0,
			"action": action,
			"errno": "memo value size is too long: (maximum size: 300 bytes, your size: {} bytes)".format(len(balance.memo))
		}

	ok = service.update(
		int(id),
		action,
		{
			"name": balance.name,
			"date": balance.date,
			"price": balance.price,
			"buy": balance.buy,
			"memo": balance.memo
		}
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
		"action": action,
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
