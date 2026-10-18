from flask import Flask, request, jsonify
import boto3
import json
import uuid

app = Flask("app")
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

@app.route('/analyze-risk', methods=['POST'])
def analyze_risk():
    data = request.json
    disruption = data.get('disruption', 'Port strike')
    region = data.get('region', 'Singapore')
    
    prompt = "You are a supply chain risk analyst. Disruption: " + disruption + " in " + region + ". Respond ONLY in JSON with: risk_level, affected_suppliers, recommended_actions, estimated_recovery_days"
    
    response = bedrock.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    
    result = response['output']['message']['content'][0]['text']
    return jsonify({"status": "success", "data": result})
