# Balance Application
- FastAPI로 제작한 가계부 시스템 입니다. (Backend)

## Requirement
- Python 3.12
- PostgreSQL
- venv
- pip

## How to use
1. 소스를 git에서 가져옵니다.
```bash
git clone https://github.com/devproje/balance-application
```

2. venv를 활성화 시켜줍니다.
- Linux 또는 macOS 사용자는 아래의 명령어를 통해 활성화를 시켜줄 수 있습니다.
```bash
./configure
```
- 또는 아래의 명령어를 이용하여 수동으로 활성화도 가능합니다.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. pip 명령어로 requiremens.txt 파일을 설치해 줍니다.
```bash
pip install -r requirements.txt
```

4. .env.example 파일을 복제하여 .env 파일을 작성해 줍니다.
- 아래의 .env 세팅은 예제 이므로 본인 환경에 맞게 작성을 해주세요.
```env
DB_URL=localhost
DB_PORT=5432
DB_DATABASE=balance
DB_USERNAME=user
DB_PASSWORD=sample1234!
```

5. fastapi 명령어를 이용하여 서비스를 실행 해줍니다.
```bash
fastapi run app.py
```
- 만약 다른 포트를 이용하셔야 한다면 아래의 명령어를 따라 주세요.
```bash
fastapi run app.py --port 3000
```

## License
본 프로젝트는 [MIT License](https://github.com/devproje/balance-application/blob/master/LICENSE)를 따릅니다.
