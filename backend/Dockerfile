FROM python:3.11-slim

LABEL maintainer="pupslchek <https://github.com/IgOrPiNgViN/foodgram-st>"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["/app/container-entry-point.sh"]
