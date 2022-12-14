FROM python:3.10
WORKDIR /usr/src/book_search
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server/ server/
ENV POSTGRES_URL=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=oreilly
ENV POSTGRES_USER=oreilly
ENV FLASK_ENV=development
ENV FLASK_APP=server/app
ENV PORT=5000
EXPOSE 5000
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000" ]