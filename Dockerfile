FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py db.py ./
COPY static ./static

ENV PYTHONUNBUFFERED=1
ENV PORT=5001
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV DB_NAME=mydb

EXPOSE 5001

CMD ["python", "app.py"]
