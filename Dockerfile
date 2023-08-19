FROM python:3.10-slim
RUN mkdir /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt

COPY src /app/src
COPY static /app/static
COPY templates /app/templates
COPY uploads /app/uploads
COPY *.py /app/
COPY *.json /app/
COPY test.py /app/

EXPOSE 7004

WORKDIR /app
# RUN ls

CMD ["python", "app.py"]

