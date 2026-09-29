FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
COPY pyproject.toml ./
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip "setuptools==78.1.1" "msgpack==1.2.1" "wheel==0.46.2" && /opt/venv/bin/pip install --no-cache-dir fastapi uvicorn[standard] pydantic pydantic-settings sqlalchemy psycopg[binary] alembic redis httpx
FROM python:3.12-slim AS runtime
ENV PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY pyproject.toml ./
COPY app ./app
COPY scripts ./scripts
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
# Build tools and the optional MessagePack codec are not needed by the running
# API. Remove them from the final image, including their bundled vendor trees,
# so the runtime contains only packages required to serve the application.
RUN /opt/venv/bin/pip uninstall --yes setuptools wheel msgpack
# The python:3.12-slim base may also ship these packages outside the venv.
# They are not runtime dependencies of CivicPulse, so remove those copies too.
RUN rm -rf \
    /usr/local/lib/python3.12/site-packages/setuptools \
    /usr/local/lib/python3.12/site-packages/setuptools-*.dist-info \
    /usr/local/lib/python3.12/site-packages/wheel \
    /usr/local/lib/python3.12/site-packages/wheel-*.dist-info \
    /usr/local/lib/python3.12/site-packages/msgpack \
    /usr/local/lib/python3.12/site-packages/msgpack-*.dist-info
# Remove any nested vendor copies left by package installers as well.
RUN find /opt/venv /usr/local/lib/python3.12/site-packages -depth \
    \( -name 'setuptools' -o -name 'setuptools-*.dist-info' \
       -o -name 'wheel' -o -name 'wheel-*.dist-info' \
       -o -name 'msgpack' -o -name 'msgpack-*.dist-info' \) \
    -exec rm -rf {} +
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
