FROM arm64v8/python:3.7.8-slim-buster

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python", "./test.py" ]