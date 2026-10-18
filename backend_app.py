from flask import Flask, request, jsonify
import boto3
import json

app = Flask("app")
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/analyze-risk', methods=['POST'])
def analyze_risk():
    try:
        data = request.json
        disruption = data.get('disruption', 'Port strike')
        region = data.get('region', 'Singapore')
        
        prompt = "You are a supply chain risk analyst. Disruption: " + disruption + " in " + region + ". Respond ONLY in valid JSON format with keys: risk_level, affected_suppliers, recommended_actions, estimated_recovery_days"
        
        response = bedrock.converse(
            modelId="amazon.nova-lite-v1:0",
            messages=[{"role": "user", "content": [{"text": prompt}]}]
        )
        
        result = response['output']['message']['content'][0]['text']
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
