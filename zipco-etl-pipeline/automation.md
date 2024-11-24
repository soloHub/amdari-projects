# Setup Automation with Cron Job on Mac

# open cron job file in your default editor
crontab -e 

# enter command below in cron file
0 6 * * * ~/Data-Engineering-Projects/amdari-projects/zipco-etl-pipeline/run_postgre_pipeline.sh

# save file 
# the python file will run every day at 6AM