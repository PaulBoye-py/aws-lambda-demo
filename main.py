import json
import boto3
import os
from datetime import datetime

# Initialize S3 client
s3_client = boto3.client('s3')

# Environment variable for bucket name
BUCKET_NAME = os.environ.get('S3_BUCKET', 'voting-eligibility-results')

def lambda_handler(event, context):
    # Extract query parameters
    query_params = event.get('queryStringParameters', {})
    name = query_params.get('name', None)
    age = query_params.get('age', None)

    # Extract body parameters if query parameters are not provided
    if not name or not age:
        body = event.get('body', '{}')
        try:
            body_data = json.loads(body)
            name = body_data.get('name', name or 'Guest')
            age = body_data.get('age', age or '0')
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON payload.'})
            }

    # Validate age input
    try:
        age = int(age)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid age. Please provide a numeric value.'})
        }

    # Determine voting eligibility
    if age >= 18:
        message = f"Hello, {name}! You are eligible to vote in the election."
    else:
        years_left = 18 - age
        message = f"Hi, {name}! You are not eligible to vote yet. You need to wait {years_left} more year(s)."

    # Save result to S3
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    result_key = f"voting_results/{timestamp}_{name}.json"
    result_data = {
        'name': name,
        'age': age,
        'message': message,
        'timestamp': timestamp
    }

    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=result_key,
            Body=json.dumps(result_data),
            ContentType='application/json'
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to save result to S3: {str(e)}"})
        }

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': message})
    }
