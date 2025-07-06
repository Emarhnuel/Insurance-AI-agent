FROM python:3.12-slim

#Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


#copy the application into the container.
COPY . /app

# Install the application dependencies
WORKDIR /app
RUN uv venv
RUN uv sync --locked

# Expose the port the app runs on
EXPOSE 800

# Run the application
CMD ["/app/.venv/bin/uvicorn", "src.insure_agent.main:app", "--port", "800", "--host", "0.0.0.0"]



