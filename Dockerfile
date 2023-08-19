FROM python:3.10-slim
RUN mkdir /app
COPY requirements.txt /app/
RUN cd /app
RUN ls
RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt

COPY src /app/src
# COPY test_frontend.py /app/

EXPOSE 7000


WORKDIR /app/src
# RUN ls

CMD ["python", "wsgi.py"]

