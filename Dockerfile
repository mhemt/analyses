FROM python:3.9

WORKDIR /analyses
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
