FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt

CMD ["python", "main.py"]