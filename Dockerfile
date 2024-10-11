FROM python:3.9
COPY . .
RUN pip install mysql-connector-python requests
RUN apt-get update && apt-get install -y curl
CMD ["python", "miniproject.py"]