# CHANGES.md

## Major Issues Identified
- Plaintext password storage
- SQL injection vulnerabilities
- Monolithic structure
- Inconsistent error handling
- Poor response formatting

## Refactoring Summary
- Modular Flask project structure
- Password hashing implemented
- SQL queries sanitized
- RESTful APIs return JSON with status codes

## Assumptions
- Basic tokenless login system retained
- SQLite remains for simplicity

## With More Time
- Add token-based auth (JWT)
- Add test cases
- Dockerize and add CI/CD
