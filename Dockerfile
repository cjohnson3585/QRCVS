FROM python:3.6


COPY src/requirements.txt ./
COPY ./qrcodes.py ./


RUN pip install -r requirements.txt


EXPOSE 8000

CMD [ "python", "./qrcodes.py" ]
