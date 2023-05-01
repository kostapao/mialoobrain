FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/
#RUN python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt  
#--no-cache-dir (add after "pip install" and before -r requirements.txt)
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader averaged_perceptron_tagger
ENV PYTHONPATH "${PYTHONPATH}:/code/app"
RUN rm -rf /code/app

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]