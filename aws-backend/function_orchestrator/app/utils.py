import json
import os
import boto3
import uuid
import time

s3_client = boto3.client('s3')
bedrock_client = boto3.client('bedrock-runtime')
sagemaker_client = boto3.client('sagemaker-runtime')
ses_client = boto3.client('ses')

# invokes sagemaker model to compute severity risk index.
def invoke_sagemaker_scorer(raw_text: str) -> int:
    try: 
        endpoint = os.environ.get('SAGEMAKER_ENDPOINT', 'threatpulse-predictive-scorer')
        payload = {"text", raw_text}
        response = sagemaker_client.invoke_endpoint(
            EndpointName = endpoint,
            ContentType = 'application/json',
            Body = json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        return int(result.get('severity_score', 45)) # safe baseline return
    except Exception as e:
        print(f"SageMaker invocation bypassed, using adaptive fallback: {e}")
        return 75 if "ransomware" in raw_text.lower() else 35
   
# coordinates aws Bedrock execution layer using anthropic claude 3.5 sonnet 
def query_bedrock_agent(company_name: str, raw_data: str, calculated_score: int) -> dict:
    prompt = '''You are the Core Reasoning Agent for an elite threat intelligence network platform.
        Target Enterprise Target Entity: {company_name}
        Upstream ML Analytical Severity Risk Index Input: {calculated_score}/100
        Harvested Raw Target Signals OSINT Stream: {raw_data}

        Synthesize the payload data assets strictly into valid structured JSON matching this exact blueprint schema:
        {{
        "primary_description": "Headline highlighting specific explicit threat vector summary",
        "category": "CRITICAL | HIGH | MEDIUM | LOW based on context and risk indexing",
        "trigger_data": ["Detailed timestamp source identifier string proofs matching telemetry timeline metrics"],
        "affected_nodes": ["Identified production system nodes, cloud VPC grids, infrastructure clusters, or named executive staff victims"],
        "ai_insight": "Comprehensive strategic breakdown explaining precisely how current intelligence maps cleanly back into recognized advanced persistent threat vectors or compromise scenarios.",
        "recommendations": ["Actionable remediation step instruction command 1", "Actionable remediation step instruction command 2"],
        "localized_locations": [{{"lat": 40.7128, "lon": -74.0060, "city": "New York"}}],
        "distributed_locations": []
        }}
        Return ONLY valid JSON. Absolutely no prose markdown text wraps or explanations.'''.format(**locals())
        
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "message": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    })
    
    response = bedrock_client.invoke_model(
        modelId = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        contentType = "application/json",
        accept = "application/json",
        body = body
    )
    
    response_body = json.loads(response.get('body').read())
    raw_output = response_body['content'][0]['text']
    return json.loads(raw_output)

# fires responsive operational alert notifications via Amazon SES
def route_ses_html_notification(target_email: str, alert_data: dict):
    subject = f"⚠️ [{alert_data['category']}] ThreatPulse Alert Notification Pipeline Activation Triggered"
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0b0f19; color: #ffffff; padding: 20px;">
        <h2 style="color: #dc3545;">ThreatPulse Core Cognitive Event Alert Frame Caught</h2>
        <p><strong>Target Enterprise Vector:</strong> {alert_data['company_name']}</p>
        <p><strong>Computed Risk Metric Index Score:</strong> {alert_data['threat_severity']}%</p>
        <p><strong>Identified Threat Classification Type:</strong> {alert_data['primary_description']}</p>
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; margin-top: 20px;">
            <h4 style="margin-top:0;">Explainable AI Diagnostics Pipeline Insight Summary:</h4>
            <p>{alert_data['ai_insight']}</p>
        </div>
    </body>
    </html>
    """
    try:
        ses_client.send_email(
            Source=target_email,
            Destination={'ToAddresses': [target_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': body_html}}
            }
        )
    except Exception as e:
        print(f"SES Alert routing bypassed during pipeline processing execution run: {e}")