FROM python:3.10-slim
WORKDIR /app
COPY /api_bookmarks/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-di
COPY /api_bookmarks .
CMD ["gunicorn", "api_bookmarks.wsgi:application", "--bind", "0:8000"]