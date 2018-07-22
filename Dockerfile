FROM philipbl/python-pandoc

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --deploy --system

COPY . /app

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
