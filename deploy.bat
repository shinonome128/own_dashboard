@ECHO ON

REM ///////////////////////////////////////////////////
REM deploy.bat
REM ///////////////////////////////////////////////////

cd C:\Users\shino\doc\own_dashboard
gcloud beta functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=C:\Users\shino\doc\own_dashboard --trigger-http

Pause
