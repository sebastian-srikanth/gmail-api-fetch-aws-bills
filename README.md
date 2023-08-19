# Fetch email attachment using gmail api
This repository guides how we can use gmail api to login to gmail and fetch details from gmail. Actually we are fetching the aws bills attachment here to analyse aws bills for future purposes.

This repo has 3 python files:

1. google_apis.py
    * To create gmail api service using Google Cloud gmail api
2. extract_text.py
    * To extract the text from pdf and save as readeble csv file for further analysis


3. main.py
    * create gmail service api objects
    * fetch all the pdf attachments from aws email
    * save pdf files under output directory
    * Extract the text from pdf and covert that to csv


Happy Coding !! :smiley: