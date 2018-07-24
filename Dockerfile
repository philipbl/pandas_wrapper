FROM philipbl/python-pandoc

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --deploy --system

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "-b", ":8000", "app:app"]