FROM philipbl/python-pandoc

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --deploy --system

COPY . /app