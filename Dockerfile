FROM python:3.7-stretch

RUN mkdir -p /code

COPY . /code

WORKDIR /code

RUN pip3 install -r requirements.txt

CMD ["python3", "crm_bot.py"]
#EXPOSE