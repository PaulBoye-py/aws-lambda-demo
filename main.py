import json

def lambda_handler(event, context):
    # Extract query parameters
    name = event.get('queryStringParameters', {}).get('name', 'Guest')
    age = event.get('queryStringParameters', {}).get('age', '0')
    
    # Validate the age input
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
