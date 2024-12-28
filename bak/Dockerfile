FROM python:3.11-alpine3.20

WORKDIR /app

RUN apk update 															\
	&& apk add --no-cache postgresql-dev gcc musl-dev make py3-uvloop 	\
	&& pip install -U pip setuptools wheel Cython

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

