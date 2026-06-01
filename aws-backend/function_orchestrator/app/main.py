import json
import os
import uuid
import time
import boto3
from app.utils import invoke_sagemaker_scorer, query_bedrock_agent, route_ses_html_notification

dynamodb = boto3.resource('dynamodb')
config_table = dynamodb.Table(os.environ.get('CONFIG_TABLE', 'ThreatPulse_Config'))
alerts_table = dynamodb.Table(os.environ.get('ALERTS_TABLE', 'ThreatPulse_Alerts'))

def lambda_handler(event, context):
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    
    # internal Cron background routing invocation hook handler route branch mapping
    if event.get('source') == 'aws.events' or path == '/scan':
        return run_background_scanning_cycle()
    
    if path == '/status' and method == 'GET':
        scan_res = config_table.scan(Limit=1)
        items = scan_res.get('Items', [])
        if items:
            return response_frame(200, {"active": True, "company_name": items[0]['company_name'], "refresh_rate": items[0]['refresh_rate']})
        
        elif path == '/setup' and method == 'POST':
            body = json.loads(event.get('body', '{}'))
            config_table.put_item(Item={
                'company_id': 'master_config',
                'company_name': body['company_name'],
                'target_email': body['target_email'],
                'refresh_rate': body['refresh_rate'],
                'toggles': body['toggles'],
                'timestamp': str(time.time())
            })
            # stimulate immdiate system bootstrap discovery event to seed the UI dashboard layout natively
            seed_mock_threat_event(body['company_name'], body['target_email'])
            return response_frame(200, {"status": "provisioned"})
            
        elif path == '/alerts' and method == 'GET':
            alerts_res = alerts_table.scan()
            return response_frame(200, {"alerts": alerts_res.get('Items', [])})
        
        elif path.startswith('/alert/') and path.endswith('/action') and method == 'POST':
            alert_id = path.split('/')[2]
            action = json.loads(event.get('body', {})).get('action')
            if action == 'resolve':
                alerts_table.update_item(
                    Key = {'alert_id': alert_id},
                    UpdateExpression="SET #s = :s, assigned_to = :e",
                    ExpressionAttributeNames={'#s': 'state'},
                    ExpressionAttributeValues={':s': 'assigned', ':e':email}
                ) 
            elif action == 'assign':
                email = json.loads(event.get('body', '{}')).get('email')
                alerts_table.update_item(
                    Key = {'alert_id': alert_id},
                    UpdateExpression="SET #s = :s, assigned_to = :e",
                    ExpressionAttributeNames={'#s': 'state'},
                    ExpressionAttributeValues={':s': 'assigned', ':e':email}
                ) 
            elif action == 'reject':
                alerts_table.delete_item(
                    Key = {'alert_id': alert_id}
                ) 
            return response_frame(200, {"status": "updated"})
        elif path == '/reset' and method == 'DELETE':
            # destructive reset switch clearing databased entities safely
            for table in [config_table, alerts_table]:
                scan = table.scan()
                for item in scan.get('Item', []):
                    key_name = 'company_id' if 'company_id' in item else 'alert_id'
                    table.delete_item(Key = {key_name: item[key_name]})
            return response_frame(200, {"status": "purged"})
        
        return response_frame(444, {"error": "Invalid network path configuration"})
    
def run_background_scanning_cycle():
    config_res = config_table.get_item(Key={'company_id': 'master_config'})
    if 'Item' not in config_res: 
        return response_frame(200, {"status": "unconfigured"})
    cfg = config_res['Item']
    
    # Benign simulated OSINT harvest signal generation stream targeting input context profiles
    simulated_onist = f"Anomalous credentials containing master security authorization headers leaked for {cfg['company_name']} inside network telemetry pipeline clusters."
    score = invoke_sagemaker_scorer(simulated_onist)
    ai_payload = query_bedrock_agent(cfg['company_name'], simulated_onist, score)
    
    alert_id = str(uuid.uuid4())
    alert_item = {
        'alert_id': alert_id,
        'company_name': cfg['company_name'],
        'threat_severity': score,
        'category': ai_payload['category'],
        'primary_description': ai_payload['primary_description'],
        'trigger_data': ai_payload['trigger_data'],
        'affected_nodes': ai_payload['affected_nodes'],
        'ai_insight': ai_payload['ai_insight'],
        'recommendations': ai_payload['recommendations'],
        'localized_locations': ai_payload['localized_locations'],
        'distributed_locations': ai_payload['distributed_locations'],
        'state': 'active'
    }
    alerts_table.put_item(Item=alert_item)
    
    if cfg['toggles'].get(ai_payload['category'].lower(), True):
        route_ses_html_notification(cfg['taget_email'], alert_item)
    
    return response_frame(200, {"status": "completed", "alert_id": alert_id})


def seed_mock_threat_event(company_name, email):
    mock_id = str(uuid.uuid4())
    item = {
        'alert_id': mock_id,
        'company_name': company_name,
        'threat_severity': 81,
        'category': 'CRITICAL',
        'primary_description': "CRITICAL - Ransomware attack signal telemetry caught on cluster infrastructure node",
        'trigger_data': ["Credential leakage source verified on dark web tracking logs 12 min ago."],
        'affected_nodes': ["3 Production Cluster Nodes", "VPC Gateway Access Frame Engine", "CEO Account Access Token Key Profile"],
        'ai_insight': "Social chatter and live credential validation spikes indicate highly coordinated multi-vector corporate intrusion targeting internal authentication stores.",
        'recommendations': ["Isolate affected asset groups immediately.", "Enforce strict system-wide enterprise password resets.", "Revoke session keys across AWS IAM root users."],
        'localized_locations': [{'lat': 44.6488, 'lon': -63.5752, 'city': 'Halifax'}],
        'distributed_locations': [],
        'state': 'active'
    }
    alerts_table.put_item(Item=item)
    route_ses_html_notification(email, item)

def response_frame(code, body):
    return{
        "statusCode": code,
        "headers": {"Content_Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body)
    }