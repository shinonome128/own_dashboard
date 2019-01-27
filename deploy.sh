#!/bin/sh

gcloud beta functions deploy main --region=us-central1 --runtime=python37 --env-vars-file conf.yml --source=./ --trigger-http
