FROM python:3.7

COPY . /code

WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 8021

CMD python app.py