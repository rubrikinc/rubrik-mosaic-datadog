# Quick Start Guide: Rubrik Mosiac Datadog Integration

Rubrik’s API first architecture enables organizations to embrace and integrate Rubrik functionality into their existing automation processes. This includes integration with services offered by modern monitoring & analytics platforms like Datadog. 

This integration allows Rubrik Mosiac customers to leverage Mosiac's APIs as well as Datadog's custom metric APIs to extract useful monitoring and reporting data out of Mosiac for presentation via Datadog dashboards.

Deployment of the solution consists of the following steps, which are covered in more detail in the sections below:

1. Deploy `rubrik-mosaic-datadog-metrics.py` to a host with access to both the Mosiac and Datadog APIs
2. Retrieve and store API keys and credentials
3. Schedule and execute the script
4. Verify metrics

## 1. Deploy the rubrik-mosaic-datadog-metrics Python script to a host with access to both the Mosiac and Datadog APIs
Clone this repository to a host with HTTPS access to the Mosiac and Datadog APIs using one of the following commands:

`git clone https://github.com/rubrikinc/rubrik-mosaic-datadog.git` 

`git clone git@github.com:rubrikinc/rubrik-mosaic-datadog.git`. 

This host will be used to schedule the script via a tool like cron. The reporing script has the following dependencies:
* Python 3.6+
* [Mosiac Python SDK](https://github.com/rubrikinc/rubrik-mosaic-sdk-for-python)
* [Datadog Python library](https://docs.datadoghq.com/integrations/python/)
* [urllib3](https://urllib3.readthedocs.io/en/latest/#)
* os, logging, datetime, and argparse modules - all part of the Python Standard Library

## 2. Retrieve and store the API keys and credentials
`rubrik-mosaic-datadog-metrics.py` takes the below parameters, most of which can be supplied via environment variables or as command line arguments upon execution. You will need to create an API and an App key within your datadog account as well as a read only user within Mosaic.

| Parameter | Description | Command Line Argument | Environment Variable |
|-----------|-------------|-----------------------|----------------------|
| help | show help message and exit | -h, --help | NA |
| Datadog API key | API key used to report custom metrics to Datadog | -api DD_API_KEY, --dd_api_key DD_API_KEY | dd_api_key |
| Datadog APP key | APP key used to report custom metrics to Datadog | -app DD_APP_KEY, --dd_app_key DD_APP_KEY | dd_app_key |
| Rubrik Mosiac IP address | IP address used to connect to Mosaic api | -i RUBRIK_MOSAIC_NODE_IP, --rubrik_mosaic_node_ip RUBRIK_MOSAIC_NODE_IP | rubrik_mosaic_node_ip |
| Rubrik Mosaic Username | Username used to connect to Mosaic api | -u RUBRIK_MOSAIC_USERNAME, --rubrik_mosaic_username RUBRIK_MOSAIC_USERNAME | rubrik_mosaic_username |
| Rubrik Mosaic Password | Password used to connect to Mosaic api | -u RUBRIK_MOSAIC_USERNAME, --rubrik_mosaic_username RUBRIK_MOSAIC_USERNAME | rubrik_mosaic_password |
| Logging enabled | Enable debug logging | -l True, --loging_enabled True | NA |
 
## 3. Schedule and execute the script
Schedule the script to run at whatever interval you would like to publish mertrics to datadog. Typically this is done via cron or a similar tool. Each execution publishes a datapoint for following values on the target Mosaic cluster as a custom metric within Datadog:
* mosaic.node_ip.protected_object_count
* mosaic.node_ip.size_under_protection
* mosaic.node_ip.secondary_storage_consumed
* mosaic.node_ip.backup_count

To run the script simply issue one of the following commands.

**Supply arguments via environment variables:**

`export rubrik_mosaic_node_ip=192.168.1.100`

`export rubrik_mosaic_username=admin`

`export rubrik_mosaic_password=admin`

`export datadog_api_key=1234567890abcdefghijklmnopqrstuv`

`export datadog_app_key=1234567890abcdefghijklmnopqrstuvwxyz1234`

`Python rubrik-mosaic-datadog-metrics.py`

**Supply arguments at runtime:**

`Python rubrik-mosaic-datadog-metrics.py -api API_KEY -app APP_KEY -i 192.168.1.100 -u USERNAME -p PASSWORD`

If you have additional metrics you would like to report on, please submit an issue on this repository!

## 4. Verify metrics
Running the script interactively with the `-l True` flag should produce `{'status': 'ok'}` for each of the `post_metrics` actions. Additionally, upon completion you will see custom metrics in your Datadog dashboard for each of the Mosaic metrics:

![image](https://user-images.githubusercontent.com/16825470/57797919-845bb080-7719-11e9-8836-9dc3d6e63437.png)
