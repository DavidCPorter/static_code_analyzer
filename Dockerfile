FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . /usr/src/app

CMD [ "python", "./hw2.py"
