FROM python:3.9
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 3000
CMD ["python","app.py"]
