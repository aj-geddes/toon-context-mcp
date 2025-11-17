---
layout: default
title: TOON Format Examples - Real-World Token Optimization Use Cases
description: Explore real-world TOON format examples showing 60% token reduction. See before/after comparisons for APIs, databases, configs, and more.
keywords: TOON examples, TOON format samples, JSON to TOON conversion examples, token optimization examples, TOON use cases
---

# TOON Format Examples

Real-world examples showing how TOON reduces token consumption across different use cases.

## API Response Optimization

### Example 1: REST API User Data

**Original JSON** (285 tokens):
```json
{
  "users": [
    {
      "id": 1001,
      "username": "alice_dev",
      "email": "alice@example.com",
      "status": "active",
      "role": "developer",
      "created_at": "2024-01-15T10:30:00Z",
      "last_login": "2025-01-17T08:22:00Z",
      "preferences": {
        "theme": "dark",
        "notifications": true,
        "language": "en"
      }
    },
    {
      "id": 1002,
      "username": "bob_designer",
      "email": "bob@example.com",
      "status": "active",
      "role": "designer",
      "created_at": "2024-02-20T14:15:00Z",
      "last_login": "2025-01-17T09:45:00Z",
      "preferences": {
        "theme": "light",
        "notifications": false,
        "language": "en"
      }
    }
  ]
}
```

**TOON Format** (142 tokens, **50% reduction**):
```json
{"_toon":"1.0","d":{"u":[{"i":1001,"un":"alice_dev","eml":"alice@example.com","s":"active","r":"developer","ca":"2024-01-15T10:30:00Z","ll":"2025-01-17T08:22:00Z","prf":{"thm":"dark","ntf":true,"lng":"en"}},{"i":1002,"un":"bob_designer","eml":"bob@example.com","s":"active","r":"designer","ca":"2024-02-20T14:15:00Z","ll":"2025-01-17T09:45:00Z","prf":{"thm":"light","ntf":false,"lng":"en"}}]}}
```

**Impact**: Fit 2x more user records in same context window.

---

## Database Query Results

### Example 2: E-commerce Orders

**Original JSON** (420 tokens):
```json
{
  "orders": [
    {
      "order_id": "ORD-2025-001",
      "customer_id": 5501,
      "order_date": "2025-01-15",
      "total_amount": 149.99,
      "currency": "USD",
      "status": "shipped",
      "items": [
        {
          "product_id": "PROD-123",
          "quantity": 2,
          "unit_price": 49.99
        },
        {
          "product_id": "PROD-456",
          "quantity": 1,
          "unit_price": 49.99
        }
      ],
      "shipping_address": {
        "street": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105"
      }
    }
  ]
}
```

**TOON Format** (198 tokens, **53% reduction**):
```json
{"_toon":"1.0","d":{"ord":[{"oi":"ORD-2025-001","ci":5501,"od":"2025-01-15","ta":149.99,"cur":"USD","s":"shipped","itm":[{"pi":"PROD-123","qty":2,"up":49.99},{"pi":"PROD-456","qty":1,"up":49.99}],"shp":{"st":"123 Main St","cty":"San Francisco","ste":"CA","z":"94105"}}]}}
```

**Impact**: Process 2.1x more orders in AI analysis tasks.

---

## Configuration Files

### Example 3: Application Config

**Original JSON** (215 tokens):
```json
{
  "application": {
    "name": "MyApp",
    "version": "2.1.0",
    "environment": "production",
    "database": {
      "host": "db.example.com",
      "port": 5432,
      "database_name": "myapp_prod",
      "connection_pool": {
        "min_connections": 5,
        "max_connections": 20,
        "timeout": 30000
      }
    },
    "cache": {
      "enabled": true,
      "redis_host": "cache.example.com",
      "redis_port": 6379,
      "ttl": 3600
    },
    "features": {
      "authentication": true,
      "rate_limiting": true,
      "analytics": false
    }
  }
}
```

**TOON Format** (105 tokens, **51% reduction**):
```json
{"_toon":"1.0","d":{"app":{"n":"MyApp","v":"2.1.0","env":"production","db":{"h":"db.example.com","p":5432,"dbn":"myapp_prod","cp":{"mnc":5,"mxc":20,"to":30000}},"cch":{"en":true,"rh":"cache.example.com","rp":6379,"ttl":3600},"ftr":{"auth":true,"rl":true,"anl":false}}}}
```

**Impact**: Larger configs fit in AI prompts without truncation.

---

## Log Data & Monitoring

### Example 4: Application Logs

**Original JSON** (310 tokens):
```json
{
  "logs": [
    {
      "timestamp": "2025-01-17T10:30:45.123Z",
      "level": "error",
      "message": "Database connection failed",
      "service": "api-gateway",
      "request_id": "req-abc-123",
      "user_id": 7890,
      "metadata": {
        "retry_count": 3,
        "error_code": "DB_CONN_TIMEOUT"
      }
    },
    {
      "timestamp": "2025-01-17T10:31:02.456Z",
      "level": "info",
      "message": "Request processed successfully",
      "service": "api-gateway",
      "request_id": "req-abc-124",
      "user_id": 7891,
      "metadata": {
        "duration_ms": 245,
        "status_code": 200
      }
    }
  ]
}
```

**TOON Format** (152 tokens, **51% reduction**):
```json
{"_toon":"1.0","d":{"logs":[{"ts":"2025-01-17T10:30:45.123Z","lvl":"error","msg":"Database connection failed","svc":"api-gateway","rid":"req-abc-123","uid":7890,"meta":{"rc":3,"ec":"DB_CONN_TIMEOUT"}},{"ts":"2025-01-17T10:31:02.456Z","lvl":"info","msg":"Request processed successfully","svc":"api-gateway","rid":"req-abc-124","uid":7891,"meta":{"dms":245,"sc":200}}]}}
```

**Impact**: Analyze 2x more log entries in debugging sessions.

---

## GitHub API Responses

### Example 5: Repository Data

**Original JSON** (380 tokens):
```json
{
  "repository": {
    "id": 12345678,
    "name": "awesome-project",
    "full_name": "user/awesome-project",
    "description": "An awesome project that does cool things",
    "private": false,
    "owner": {
      "login": "user",
      "id": 9876543,
      "type": "User"
    },
    "html_url": "https://github.com/user/awesome-project",
    "created_at": "2024-06-15T08:30:00Z",
    "updated_at": "2025-01-17T12:00:00Z",
    "pushed_at": "2025-01-17T11:45:00Z",
    "size": 2048,
    "stargazers_count": 142,
    "watchers_count": 28,
    "language": "Python",
    "forks_count": 19,
    "open_issues_count": 7,
    "license": {
      "key": "mit",
      "name": "MIT License"
    },
    "topics": ["python", "automation", "devtools"]
  }
}
```

**TOON Format** (185 tokens, **51% reduction**):
```json
{"_toon":"1.0","d":{"repo":{"i":12345678,"n":"awesome-project","fn":"user/awesome-project","dsc":"An awesome project that does cool things","prv":false,"own":{"lgn":"user","i":9876543,"t":"User"},"url":"https://github.com/user/awesome-project","ca":"2024-06-15T08:30:00Z","ua":"2025-01-17T12:00:00Z","pa":"2025-01-17T11:45:00Z","sz":2048,"strs":142,"wtch":28,"lng":"Python","frks":19,"iss":7,"lic":{"k":"mit","n":"MIT License"},"tpc":["python","automation","devtools"]}}}
```

**Impact**: Integrate more GitHub data in AI-powered code analysis.

---

## Token Savings Calculator

Use these real-world patterns to estimate your savings:

| Data Type | Typical Size | Token Reduction | Savings |
|-----------|--------------|-----------------|---------|
| User profiles | 200-400 tokens | 50-55% | 100-220 tokens |
| API responses | 300-600 tokens | 48-58% | 150-350 tokens |
| Config files | 150-300 tokens | 45-52% | 70-155 tokens |
| Log entries | 100-200 tokens | 40-50% | 40-100 tokens |
| Database records | 250-500 tokens | 52-60% | 130-300 tokens |

---

## Integration Examples

### Python Usage

```python
from src.toon_converter import convert_json_to_toon, convert_toon_to_json

# Convert API response
api_response = {"users": [...]}  # Your JSON data
toon_format = convert_json_to_toon(api_response)

# Use in AI prompt
prompt = f"Analyze this user data: {toon_format}"

# Convert back if needed
original = convert_toon_to_json(toon_format)
```

### MCP Tool Usage in Claude

```
Use the convert_to_toon tool:
- json_data: { "your": "data" }
- aggressive: true

Result shows token savings and TOON format ready for conversation.
```

---

## Try These Examples

1. **[Install TOON-MCP]({{ '/guides/setup' | relative_url }})** - Get started in 5 minutes
2. **[Read User Guide]({{ '/guides/user-guide' | relative_url }})** - Learn advanced techniques
3. **[API Reference]({{ '/api/reference' | relative_url }})** - Full documentation

---

## Share Your Results

Achieved impressive token savings with TOON? Share your use case on [GitHub Discussions](https://github.com/aj-geddes/toon-context-mcp/discussions)!

<div class="alert alert-success">
<strong>💡 Pro Tip</strong><br>
TOON works best with repeating data structures. The more items in your arrays, the better the compression ratio!
</div>
