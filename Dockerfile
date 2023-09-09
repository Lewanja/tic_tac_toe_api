FROM python
WORKDIR /app
COPY tic_tac_toe /app
RUN pip install -r requirements.txt
COPY tic_tac_toe .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]