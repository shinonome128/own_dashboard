@ECHO ON

REM ///////////////////////////////////////////////////
REM destroy.bat
REM ///////////////////////////////////////////////////

cd C:\Users\shino\doc\own_dashboard  
gcloud beta functions delete main --region=us-central1  

Pause
