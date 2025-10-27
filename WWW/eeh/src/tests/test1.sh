curl -X POST http://localhost:3000/users/login \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "password123"}'