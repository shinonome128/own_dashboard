#!/bin/sh

gcloud auth activate-service-account --key-file gcf-demo-2b39da7a07dd.json  
gcloud beta functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=./ --trigger-http
