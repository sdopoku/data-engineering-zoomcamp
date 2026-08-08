# Start with a current slim Python 3.13 image on a supported Debian release
FROM python:3.13-slim-bookworm

# Copy uv binary from the official uv image using a pinned release
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
# COPY "pyproject.toml" "uv.lock" ".python-version" ./
COPY ../ ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]