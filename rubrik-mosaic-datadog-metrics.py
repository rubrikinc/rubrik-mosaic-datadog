import os
from datadog import initialize, api
import rubrik_mosaic
import urllib3
import logging
import datetime
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Upload the following Rubrik Mosaic metrics to Datadog as custom metrics: protected_object_count, size_protected_MB, secondary_storage_consumed_MB, backup_count.")
parser.add_argument("-api","--dd_api_key", help="Datadog api key, if not defined will default to environment variable 'dd_api_key'")
parser.add_argument("-app","--dd_app_key", help="Datadog app key, if not defined will default to environment variable 'dd_app_key'")
parser.add_argument("-i","--rubrik_mosaic_node_ip", help="mosaic node ip address, if not defined will default to environment variable 'rubrik_mosaic_node_ip'")
parser.add_argument("-u","--rubrik_mosaic_username", help="mosaic username, if not defined will default to environment variable 'rubrik_mosaic_username'")
parser.add_argument("-p","--rubrik_mosaic_password", help="mosaic password, if not defined will default to environment variable 'rubrik_mosaic_password'")
parser.add_argument("-l","--logging_enabled", help="enable or disable debug logging", type=bool)
args = parser.parse_args()

##User Defined Variables##
#api/app keys used to connect to datadog api
#can also be specified via env vars dd_api_key and dd_app_key
dd_api_key = args.dd_api_key
dd_app_key = args.dd_app_key
#ip, username, and password used to connect to mosaic api
#can also be specified via env vars rubrik_mosaic_node_ip, rubrik_mosaic_username, and rubrik_mosaic_password
rubrik_mosaic_node_ip = args.rubrik_mosaic_node_ip
rubrik_mosaic_username = args.rubrik_mosaic_username
rubrik_mosaic_password = args.rubrik_mosaic_password
#debug logging
if args.logging_enabled:
    logging_enabled=args.logging_enabled
else:
    logging_enabled=False

if logging_enabled:
    #debug logging
    console_output_handler = logging.StreamHandler()
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] -- %(message)s")
    console_output_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.addHandler(console_output_handler)
    def log(log_message):
        logger.debug(log_message)

def connect_datadog(api_key=None, app_key=None):
    #If the api_key and app_key has not been provided check for the env variable
    if api_key is None:
        api_key = os.environ.get('dd_api_key')
        if api_key is None:
            raise ValueError("The Datadog api key has not been provided.")
    if app_key is None:
        app_key = os.environ.get('dd_app_key')
        if app_key is None:
                raise ValueError("The Datadog app key has not been provided.")
    #connect to datadog api
    options = {
        'api_key': api_key,
        'app_key': app_key
    }
    initialize(**options)

#connect to datadog
connect_datadog(dd_api_key, dd_app_key)

#connect to mosaic cluster
rubrik = rubrik_mosaic.Connect(node_ip=rubrik_mosaic_node_ip, username=rubrik_mosaic_username,password=rubrik_mosaic_password, enable_logging=logging_enabled)

def post_metrics(rubrik, enable_logging=False):
    #dict to iterate metrics 
    metrics = {}
    #get number of objects protected via mosaic
    if enable_logging:
        log('post_metrics - getting protected_object_count')
    metrics['protected_object_count'] = rubrik.get_protected_object_count()
    if enable_logging:
        log('post_metrics - protected_object_count: {}'.format(metrics['protected_object_count']))
    #get size under protection
    if enable_logging:
        log('post_metrics - getting size_protected')
    metrics['size_protected_MB'] = rubrik.get_size_under_protection()
    if enable_logging:
        log('post_metrics - size_protected_MB: {}'.format(metrics['size_protected_MB']))
    #get secondary storage consumed
    if enable_logging:
        log('post_metrics - getting secondary_storage_consumed')
    metrics['secondary_storage_consumed_MB'] = rubrik.get_secondary_storage_consumed()
    if enable_logging:
        log('post_metrics - secondary_storage_consumed_MB: {}'.format(metrics['secondary_storage_consumed_MB']))
    #get total number of backups
    if enable_logging:
        log('post_metrics - getting backup_count')
    metrics['backup_count'] = rubrik.get_backup_count()
    if enable_logging:
        log('post_metrics - backup_count: {}'.format(metrics['backup_count']))
    for metric, value in metrics.items():
        if enable_logging:
            log('post_metrics - posting {} to datadog api for mosaic cluster {}'.format(metric, rubrik.node_ip))
        response = api.Metric.send(metric="mosaic.{}.{}".format(rubrik.node_ip, metric), points=value)
        if enable_logging:
            log('post metrics - {}'.format(response))

post_metrics(rubrik, enable_logging=logging_enabled)