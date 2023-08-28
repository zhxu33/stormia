FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]

#docker build -t stormia-bot .
#docker run stormia-bot