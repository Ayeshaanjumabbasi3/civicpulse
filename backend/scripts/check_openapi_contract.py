"""Check the frontend-facing contract against FastAPI's generated OpenAPI schema."""

from app.main import app

required = {
    "/api/complaints": {"get", "post"},
    "/api/complaints/{complaint_id}": {"get"},
    "/api/complaints/{complaint_id}/status": {"patch"},
    "/api/stats": {"get"},
    "/api/meta/providers": {"get"},
    "/api/meta/contract": {"get"},
    "/health": {"get"},
    "/ready": {"get"},
    "/metrics": {"get"},
}
schema = app.openapi()
paths = schema["paths"]
missing = [
    f"{method.upper()} {path}"
    for path, methods in required.items()
    for method in methods
    if method not in paths.get(path, {})
]
if missing:
    raise SystemExit("Missing OpenAPI operations: " + ", ".join(missing))
print(f"OpenAPI contract verified: {sum(len(x) for x in required.values())} operations")
