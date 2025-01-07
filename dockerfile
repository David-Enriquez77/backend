FROM python:3.13.0
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /code/
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]