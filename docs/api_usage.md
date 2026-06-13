# API Usage Guide

Base URL: `http://localhost:8000/api/v1`

## Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"investor@example.com\",\"full_name\":\"Investor\",\"password\":\"strongpass123\"}"
```

## Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"investor@example.com\",\"password\":\"strongpass123\"}"
```

## Create Portfolio

```bash
curl -X POST http://localhost:8000/api/v1/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Long Term Wealth\"}"
```

## Generate Recommendations

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"investment_amount\":100000,\"candidates\":[{\"ticker\":\"TCS\"},{\"ticker\":\"INFY\"}]}"
```
