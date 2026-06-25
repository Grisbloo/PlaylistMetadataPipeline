#where it comes from
FROM python:3.11-slim
#folder which we create to put the files in /app is standard
WORKDIR /app
#place what you want where you want (this file here is . .)
COPY . .
#What it is that needs to be run prior to the actual code
RUN apt-get update && apt-get install -y chromium chromium-driver && pip install -r requirements.txt
#The code that needs to be run
CMD [ "python", "main.py" ]