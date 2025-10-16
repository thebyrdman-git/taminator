FROM python:3.11-slim

LABEL maintainer="jbyrd@redhat.com"
LABEL description="GitLab Webhook Receiver for PAI RFE & Bug Tracker"
LABEL version="1.0.0"

# Install dependencies
RUN pip install --no-cache-dir flask

# Create app directory
WORKDIR /app

# Create logs directory
RUN mkdir -p /app/logs

# Copy application
COPY gitlab_webhook_receiver.py /app/

# Expose webhook port
EXPOSE 3002

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:3002/health')"

# Run application
CMD ["python3", "-u", "gitlab_webhook_receiver.py"]

