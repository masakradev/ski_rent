FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY . /app
COPY /app/static /app/static

RUN pip install -r requirements.txt