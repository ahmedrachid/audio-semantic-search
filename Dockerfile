FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
COPY streamlit_audio.py ./
COPY gp_icon.png ./

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit_audio.py", "--server.port=8501", "--server.address=0.0.0.0"]
