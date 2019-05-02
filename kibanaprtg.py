import requests
import json
import sys
from paepy.ChannelDefinition import CustomSensorResult


if __name__ == "__main__":
	#load the prtg parameters into a dictionary and make call to ES host
	data = json.loads(sys.argv[1])
	url = 'http://{0}:5601/api/status'.format(data['host'])
	req = requests.get(url)
	
	#load the json response into a dictionary
	output = json.loads(req.text)
	
    #Turn status colour into a number so that it can be viewed in prtg
	color = output['status']['overall']['state']
	if color == 'green':
		status = 0
	elif color == 'yellow':
		status = 1
	elif color == 'red':
		status = 2


    # create a prtg sensor and add the channel data. Each key/value in the json response from ES gets channelised
	sensor = CustomSensorResult(output['status']['overall']['state'])
	sensor.add_channel(channel_name="Status", unit="Count", value=status, is_limit_mode=True, limit_max_error=1.5,limit_max_warning=0.5)
	sensor.add_channel(channel_name="Metrics Requests Total", unit="Count", value=output['metrics']['requests']['total'])
	sensor.add_channel(channel_name="Metrics Connections", unit="Count", value=output['metrics']['concurrent_connections'])
	sensor.add_channel(channel_name="Max. Response Time", unit="Milliseconds", value=output['metrics']['response_times']['max_in_millis'])
	sensor.add_channel(channel_name="Avg. Response Time", unit="Milliseconds", value=output['metrics']['response_times']['avg_in_millis'])

    # send the sensor data back to the prtg process in json format
	print(sensor.get_json_result())
