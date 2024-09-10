from datetime import datetime
from fastapi import APIRouter, Response
from service.balance_service import Balance, BalanceService, UpdateForm

router = APIRouter()

@router.post("/balance", status_code=201)
def insert(balance: Balance, resp: Response):
	started = datetime.now().microsecond / 1000
	service = BalanceService()
	ok = service.create(balance=balance)
	if not ok == 1:
		resp.status_code = 500
		return {
			"ok": 0,
			"errno": "error occurred to running transaction"
		}

	return {
		"ok": 1,
		"name": balance.name,
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.get("/balance/{id}")
def query(id, resp: Response):
	started = datetime.now().microsecond / 1000
	service = BalanceService()

	try:
		data = service.read(int(id))
	except:
		resp.status_code = 204
		return {"ok": 0, "errno": "id '{}' result is not found".format(id)}

	return {
		"ok": 1,
		"id": int(id),
		"data": data,
		"respond_time": "{}ms".format(round((datetime.now().microsecond / 1000) - started))
	}

@router.patch("/balance/{action}/{id}")
def update(action, id, balance: UpdateForm, resp: Response):
	service = BalanceService()
	if action != "name" and action != "date" and action != "price" and action != "memo":
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
		action, {
			"name": balance.name,
			"date": balance.date,
			"price": balance.price,
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
		"action": action
	}

@router.delete("/balance/{id}")
def delete(id, resp: Response):
	started = datetime.now().microsecond / 1000
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
