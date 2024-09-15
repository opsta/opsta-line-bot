FROM python:3.12.6-bookworm AS build
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=packages -r requirements.txt


FROM python:3.12.6-slim-bookworm AS runtime
# Copying Dependencies from build stage
COPY --from=build packages /usr/local/lib/python3.12/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

USER 65532
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python healthcheck.py

WORKDIR /app
COPY chat.py healthcheck.py ./
EXPOSE 5000
ENTRYPOINT ["python", "-m", "flask", "--app", "chat", "run", "--host=0.0.0.0", "--port=5000"]
