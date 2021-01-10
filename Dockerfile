FROM python:3.6
WORKDIR /opt
COPY bennys-bot.py /opt
RUN pip3 install -U discord.py
RUN pip3 install requests
ENTRYPOINT [ "/usr/local/bin/python3", "bennys-bot.py" ]