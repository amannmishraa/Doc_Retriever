FROM python:3.9

WORKDIR /app

ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME DocumentRetrievalApp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
