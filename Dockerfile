FROM --platform=linux/amd64 python:3.12-slim

#Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


#copy the application into the container.
COPY . /app

# Install the application dependencies
WORKDIR /app
RUN uv venv
RUN uv sync --locked

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["/app/.venv/bin/uvicorn", "insure_agent.main:app", "--port", "8000", "--host", "0.0.0.0", "--app-dir", "/app/src"]
