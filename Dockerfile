FROM python:3.8

WORKDIR /usr/src/app

COPY Pipfile.lock .
COPY Pipfile .

RUN pip install -U pip pipenv && pipenv install --system --deploy --ignore-pipfile --dev

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3", "asgi.py"]
