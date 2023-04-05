FROM python:3.9-slim

WORKDIR /foodgram

COPY . .

RUN apt-get update

RUN python3 -m pip install --upgrade pip --no-cache-dir

RUN pip3 install -r requirements.txt --no-cache-dir

RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]