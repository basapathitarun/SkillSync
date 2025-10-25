# ---- Base Image ----
FROM python:3.11-slim

# ---- Install uv ----
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# ---- Set working directory ----
WORKDIR /app

# ---- Copy project files ----
COPY . /app

# ---- Install dependencies using uv ----
RUN uv sync --frozen

# ---- Expose port ----
EXPOSE 8000

# ---- Run FastAPI app ----
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
