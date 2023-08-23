FROM python:3.9-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code/
CMD ["python", "main.py"]