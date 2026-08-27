#!/bin/bash
BASE_URL="http://127.0.0.1:8000"

curl -X GET "$BASE_URL/health/live"
echo -e "\n"
curl -X GET "$BASE_URL/health/ready"
echo -e "\n"
curl -X POST "$BASE_URL/todos" \
	-H "Content-Type: application/json" \
	-d '{"title":"FastAPI", "description":"10582782026", "priority":3, "completed":true}'
echo -e "\n"
curl -X POST "$BASE_URL/todos" \
	-H "Content-Type: application/json" \
	-d '{"title":"Test", "priority":2, "completed":true}'
echo -e "\n"
curl -X GET "$BASE_URL/todos"
echo -e "\n"
curl -X GET "$BASE_URL/todos/1"
echo -e "\n"
curl -X PUT "$BASE_URL/todos/1" \
	-H "Content-Type: application/json" \
	-d '{"title": "FastAPI nang cao", "completed": true}'
echo -e "\n"
curl -X DELETE "$BASE_URL/todos/1"
echo -e "\n"
curl -X GET "$BASE_URL/todos"
