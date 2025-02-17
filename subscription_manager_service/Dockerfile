FROM python:3.12-slim

WORKDIR /app

RUN apt-get clean && apt-get update && apt-get install -y \ 
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5030

CMD ["flask", "run", "--host=0.0.0.0", "--port=5030"]