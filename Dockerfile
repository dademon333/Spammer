FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip wheel setuptools \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .
