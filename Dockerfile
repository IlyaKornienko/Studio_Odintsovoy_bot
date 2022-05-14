FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip && pip install pyTelegramBotAPI && pip install types-all  && pip install vedis 
COPY *.py ./

ENTRYPOINT ["python", "bot.py"]

