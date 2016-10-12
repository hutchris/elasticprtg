# Elasticmon
Simple API to PRTG sensor script for Elasticsearch cluster health data

This script uses the data returned by Elasticsearch when you do a call to http://{ESNODEIP}:9200/_cluster/health and turns each key/value pair into a channel inside a PRTG sensor

You need to install the requests module to the python instance that comes with PRTG. The easiest way to do this is to install pip.

  1. Download the get-pip.py file from here: https://pip.pypa.io/en/stable/installing/
  2. Open cmd as admin and run: C:\Program Files (x86)\PRTG Network Monitor\Python34\python.exe [path to file]\get-pip.py
  3. You can then run C:\Program Files (x86)\PRTG Network Monitor\Python34\Scripts\pip.exe install requests
  
Once installed, paste the elasticprtg.py file to the custom sensors directory on the PRTG machine that will be doing the query. If you have remote probes, it will have to be on those machines. The custom sensor directory is found here: 
C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python

If you're not already monitoring an ES node from your cluster you will need to add it to PRTG first. Then you can add this as a "python script advanced" sensor and pick the elasticprtg.py file from the drop down. 

You should then see the results show up in PRTG. You should set appropriate warning and error limits on the channels that you want to be alerted about.
