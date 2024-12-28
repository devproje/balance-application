# Balance Application
- Gin으로 제작한 가계부 시스템 입니다. (Backend)
- 클라이언트
	- [Balance Client](https://github.com/devproje/balance-client) - API 불일치로 작동 안함

## Requirement
- Go >= 1.23.4
- PostgreSQL

## How to use
- ~~빌드 결과물은 [Releases](https://github.com/devproje/balance-application/releases)탭을 확인 해주세요!~~ (Github Actions 준비중)

## How to build
1. 소스를 git에서 가져옵니다.
```bash
git clone https://github.com/devproje/balance-application
```

2. 라이브러리를 불러와 줍니다.
- Linux 또는 macOS 사용자는 아래의 명령어를 통해 활성화를 시켜줄 수 있습니다.
```bash
./configure
```

4. config.sample.json 파일을 복제하여 config.json 파일을 작성해 줍니다.
- 아래의 config.json 세팅은 예제 이므로 본인 환경에 맞게 작성을 해주세요.
```json
{
	"port": 8080,
	"signup": false,
	"salt_size": 10,
	"db_data": {
		"host": "localhost",
		"port": 5432,
		"db_name": "balance",
		"username": "user",
		"password": "pass"
	}
}
```
- 보안을 위해 signup 변수는 최초 계정 생성할때 빼고는 끄도록 합니다.

5. Makefile을 이용하여 빌드를 해주세요.
```bash
make
```
- 만약 makefile 시스템이 없는 경우에는 아래의 명령어를 입력 해주세요!
```bash
go build -o balance-application
```

6. 아래의 명령어로 빌드 결과물을 실행 합니다.
```bash
./balance-application
```
- 만약 디버깅 모드를 사용하고 싶으시다면 아래의 명령어를 따라 주시면 됩니다.
```bash
# full argument
./balance-application --debug
# or short argument
./balance-application -d
```

## License
본 프로젝트는 [MIT License](https://github.com/devproje/balance-application/blob/master/LICENSE)를 따릅니다.
