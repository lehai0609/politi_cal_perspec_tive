FROM python:3.11-slim
WORKDIR /app
COPY .. /app
RUN pip install --no-cache-dir fastapi uvicorn[standard] spacy \
    && python -m spacy download en_core_web_sm
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
