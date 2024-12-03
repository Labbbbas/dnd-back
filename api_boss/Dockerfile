FROM python:3.13.0-alpine3.20

WORKDIR /app

# Create a new user group and user with specific UID and GID
RUN addgroup -g 1000 app && adduser -D -u 1000 -G app app

# Copy the application code to the working directory and set ownership to the app user
COPY --chown=app . .

# Update package index, install dependencies, and Python packages
RUN apk update && \
    apk add --no-cache curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn Flask flask-cors pymongo marshmallow flasgger

# Create the log file, set permissions, and assign ownership to the app user
RUN touch /app/boss_api.log && chmod 666 /app/boss_api.log && chown app:app /app/boss_api.log

# Expose the application port
EXPOSE 8000

# Define a health check for the application
HEALTHCHECK CMD curl --fail http://localhost:8000/healthcheck || exit 1

# Switch to the non-root user
USER app

# Define the entry point for the container
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "-w 4", "app:app" ]
