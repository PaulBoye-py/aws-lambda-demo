import json

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

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': message})
    }
