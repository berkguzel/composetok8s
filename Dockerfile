FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]


