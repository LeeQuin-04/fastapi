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

# 2. Khoi chay server tron Ter thu nhat
uv run uvicorn main:app --reload
Server: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
7 enpoints:
	GET /health/live -> Xac nhan server dng chay
	GET /health/ready -> Kiem tra ket noi db
	GET /todos -> Lay toan bo danh sach 
	POST /todos -> Tao mot Todos moi
	GET /todos/{todo_id} -> Lay thong tin chi tiet cua Todos co id la todo_id
	PUT /todos/{todo_id} -> Cp nhat Todos co id la todo_id
	DELETE /todos/{todo_id} -> Xoa Todos co id la todo_id

## Chay script test voi curl trong Ter thu hai
chmod +x curl.sh
./curl.sh

## Log tra ve minh hoa luong goi API

1. Kiem tra Health
{"status":"Song rat khoe"}

{"status":"San sang","database":"Da ket noi"}


2. Tao moi 2 Todos
{"title":"FastAPI","description":"10582782026","completed":true,"priority":3,"id":1}

{"title":"Test","description":null,"completed":true,"priority":2,"id":2}


3. Lay danh sach toan bo Todos
[{"title":"FastAPI","description":"10582782026","completed":true,"priority":3,"id":1},{"title":"Test","description":null,"completed":true,"priority":2,"id":2}]


4. Lay chi tiet Todo co ID = 1
{"title":"FastAPI","description":"10582782026","completed":true,"priority":3,"id":1}


5. Cap nhat thong tin Todo ID = 1
{"title":"FastAPI nang cao","description":"10582782026","completed":true,"priority":3,"id":1}


6. Xoa Todo co ID = 1
(HTTP 204 No Content)


7. Kiem tra lai danh sach Todos sau khi xoa ID = 1
[{"title":"Test","description":null,"completed":true,"priority":2,"id":2}]
