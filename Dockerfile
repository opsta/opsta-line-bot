# SECURITY VULNERABILITY
# FROM python:3.12.0-bookworm AS build
FROM python:3.12.7-bookworm AS build
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=packages -r requirements.txt


# SECURITY VULNERABILITY
# FROM python:3.12.0-slim-bookworm AS runtime
FROM python:3.12.7-slim-bookworm AS runtime
# Copying Dependencies from build stage
COPY --from=build packages /usr/local/lib/python3.12/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

USER 65532
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "healthcheck.py"]

WORKDIR /app
COPY chat.py healthcheck.py ./
EXPOSE 5000
ENTRYPOINT ["python", "-m", "gunicorn", "chat:app", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]
CMD ["-w", "1"]
