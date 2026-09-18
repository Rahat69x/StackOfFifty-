"""
Audit logging and security headers middleware for FastAPI.
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from core.logger import get_logger
from core.database.connection import SessionLocal
from core.database.models import AuditLog

logger = get_logger("api.middleware")

class LoggingAndAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        # Inject standard security headers (spec page 51)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"

        # Audit mutable or sensitive operations
        if method in ("POST", "PUT", "DELETE", "PATCH") and not path.startswith("/api/auth/login"):
            try:
                db = SessionLocal()
                audit_entry = AuditLog(
                    action=f"{method} {path}",
                    target=path,
                    ip_address=client_ip,
                    details={"status_code": response.status_code, "latency_ms": round(process_time, 2)}
                )
                db.add(audit_entry)
                db.commit()
                db.close()
            except Exception as e:
                logger.warning(f"Could not persist audit record: {e}")

        logger.info(f"{method} {path} - {response.status_code} ({process_time:.1f}ms)")
        return response
