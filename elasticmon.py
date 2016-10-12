import requests
import json
import sys
from paepy.ChannelDefinition import CustomSensorResult


if __name__ == "__main__":
	#load the prtg parameters into a dictionary and make call to ES host
	data = json.loads(sys.argv[1])
	url = 'http://{0}:9200/_cluster/health'.format(data['host'])
	req = requests.get(url)
	
	#load the json response into a dictionary
	output = json.loads(req.text)
	
	#Turn status colour into a number so that it can be viewed in prtg
	if output['status'] == 'green':
		status = 0
	elif output['status'] == 'yellow':
		status = 1
	elif output['status'] == 'red':
		status = 2
	
	#turn timed out into a number so that it can be viewed in prtg
	if output['timed_out'] == False:
		timedOut = 0
	else:
		timedOut = 1
		
	#create a prtg sensor and add the channel data. Each key/value in the json response from ES gets channelised
	sensor = CustomSensorResult(output['status'])
	sensor.add_channel(channel_name="Status",unit="Count",value=status,is_limit_mode=True,limit_max_error=1.5,limit_max_warning=0.5)
	sensor.add_channel(channel_name="Number Of Data Nodes",unit="Count",value=output['number_of_data_nodes'])
	sensor.add_channel(channel_name="Number of Nodes",unit="Count",value=output['number_of_nodes'])
	sensor.add_channel(channel_name="Percent of Shards Active",unit="Percent",value=output['active_shards_percent_as_number'])
	sensor.add_channel(channel_name="Delayed Unassigned Shards",unit="Count",value=output['delayed_unassigned_shards'])
	sensor.add_channel(channel_name="In Flight Fetches",unit="Count",value=output['number_of_in_flight_fetch'])
	sensor.add_channel(channel_name="Relocating Shards",unit="Count",value=output['relocating_shards'])
	sensor.add_channel(channel_name="Pending Tasks",unit="Count",value=output['number_of_pending_tasks'])
	sensor.add_channel(channel_name="Initializing Shards",unit="Count",value=output['initializing_shards'])
	sensor.add_channel(channel_name="Unassigned Shards",unit="Count",value=output['unassigned_shards'])
	sensor.add_channel(channel_name="Task Queue Time (max)",unit="Milliseconds",value=output['task_max_waiting_in_queue_millis'])
	sensor.add_channel(channel_name="Timed Out",unit="Count",value=timedOut,is_limit_mode=True,limit_max_error=0.5,limit_error_msg="Timed Out = True")
	
	#send the sensor data back to the prtg process in json format
	print(sensor.get_json_result())
