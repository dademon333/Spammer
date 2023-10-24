FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip wheel setuptools \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
