FROM python

WORKDIR /app

COPY . .

RUN pip install mysql-connector

RUN pip install discord.py

CMD ["python", "bot.py"]