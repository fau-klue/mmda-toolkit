export TOKEN=$(curl -H 'Content-Type: application/json' -X POST http://localhost:5000/api/login/ -d '{"username": "admin", "password": "Squanchy1"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")


curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-login/

curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X POST http://localhost:5000/api/user/admin/discourseme/ -d '{"name": "Atomkraft", "items": ["Atomkraft", "Atomkraftwerk", "Atomenergie", "Kernkraft", "Kernkraftwerk", "Kernenergie", "Nuklearenergie"]}'
