FROM python:3.8

RUN mkdir -p /usr/src/
WORKDIR /usr/src/

COPY . /usr/src/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python manage.py makemigrations --no-input \
            && python manage.py migrate --no-input \
            && python manage.py runserver 0.0.0.0:8000

EXPOSE 8000