FROM python:3.9

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install sentence-transformers==2.2.2

COPY . /code/

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
