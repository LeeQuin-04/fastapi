## Cấu trúc dữ liệu Todo (Schema)

`id` : `Integer` : Khoa chinh (primary key) tu dong tang
`title` : `String` : Tieu de (0 < so ky tu <= 255)
`description` : `String` : Mo ta
`priority` : `Integer` : Do uu tien
`completed` : `Boolean` : Trng thai hoan thanh

## Cai dat & Khoi chay
```bash
# 1. Cai dat dependencies
uv sync

# 2. Khoi chay server
uv run uvicorn main:app --reload
Server: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
7 enpoints:
	GET /health/live
	GET /health/ready
	GET /todos
	POST /todos
	GET /todos/{todo_id}
	PUT /todos/{todo_id}
	DELETE /todos/{todo_id}

## Chay script test voi curl
+x curl.sh
./curl.sh
