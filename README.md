# Voting Eligibility Checker - AWS Lambda with S3 Integration

## Overview

This Lambda function determines if a user is eligible to vote based on their age. It also saves the result of each eligibility check to an S3 bucket. The function supports input via query parameters or a JSON payload in the request body.

### Key Features

- Checks if a user meets the minimum voting age (18 years).
- Provides a customized response based on the user's eligibility.
- Saves eligibility results to an Amazon S3 bucket for future reference.

---

## Requirements

- **AWS Lambda**: Used to deploy and execute the function.
- **Amazon S3**: Stores the results of the eligibility checks.
- **Python 3.8 or above**: Runtime for the function.

---

## Environment Variables

The function uses the following environment variables:

- **`S3_BUCKET`**: Name of the S3 bucket where results will be saved. Defaults to `voting-eligibility-results`.

---

## How It Works

1. **Input Handling**  
   - Extracts user data (`name` and `age`) from query parameters or JSON payload in the request body.
   - Defaults `name` to "Guest" and `age` to "0" if not provided.

2. **Eligibility Check**  
   - Validates the age input to ensure it is numeric.
   - Determines voting eligibility based on whether the user's age is 18 or older.

3. **Save Results to S3**  
   - Constructs a JSON object containing the user's name, age, eligibility message, and a timestamp.
   - Stores the result in an S3 bucket under the key structure: `voting_results/<timestamp>_<name>.json`.

4. **Response**  
   - Returns an HTTP response with the eligibility message.

---

## Deployment Instructions

### Prerequisites

1. **Amazon S3 Bucket**: Create an S3 bucket and note its name.
2. **IAM Role for Lambda**: Ensure the Lambda execution role has permissions to write to the S3 bucket. Example policy:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:PutObject",
         "Resource": "arn:aws:s3:::<bucket-name>/voting_results/*"
       }
     ]
   }
   ```

### Deploy the Function

1. **Create a Lambda Function**:
   - Runtime: Python 3.8 or above.
   - Handler: `lambda_function.lambda_handler`.

2. **Set Environment Variables**:
   - `S3_BUCKET`: The name of your S3 bucket.

3. **Upload the Code**:
   - Zip the code file and upload it to AWS Lambda.

4. **Test the Function**:
   - Use the following sample event:

     ```json
     {
       "queryStringParameters": {
         "name": "Paul",
         "age": "20"
       }
     }
     ```

---

## API Example Usage

### Input

- **HTTP Method**: POST
- **Endpoint**: `<API Gateway URL>`
- **Query Parameters**:
  - `name`: User's name (optional, default: "Guest").
  - `age`: User's age (optional, default: 0).

- **Request Body (if query parameters are not provided)**:

  ```json
  {
    "name": "Paul",
    "age": 20
  }
  ```

### Output

- **200 OK**:

  ```json
  {
    "message": "Hello, Paul! You are eligible to vote in the election."
  }
  ```

- **400 Bad Request** (Invalid Age):

  ```json
  {
    "error": "Invalid age. Please provide a numeric value."
  }
  ```

- **500 Internal Server Error** (S3 Failure):

  ```json
  {
    "error": "Failed to save result to S3: <error message>"
  }
  ```

---

## Directory Structure

```bash
.
├── lambda_function.py  # Main function file
└── requirements.txt    # Python dependencies (if applicable)
```

---

## S3 Bucket Policy Template

To grant Lambda permission to write to the S3 bucket, use the following S3 bucket policy:

### **S3 Bucket Policy**

```json
{
  "Id": "Policy1737224295164",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1737224291425",
      "Action": "s3:*",
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::<your-bucket-name>/voting_results/*",
      "Principal": "*"
    }
  ]
}
```

### **Explanation**

- **`Action`**: Grants the `s3:*` action, allowing the Lambda function to interact with the specified S3 bucket.
- **`Resource`**: Specifies the path where the Lambda function can put objects (`voting_results/*`).
- **`Principal`**: The `"*"` value means this policy is not restricted by any particular principal, which is standard when granting access to a service (like Lambda).

### **Ensure Public Access is Not Blocked**

- When configuring the S3 bucket, make sure **public access is not blocked** to allow the Lambda function to write results into the bucket.
- To maintain security, you can restrict access further by specifying the AWS account or Lambda function ARN in the `Principal` section.

---

## Improvements

- Add authentication to secure the API.
- Extend the functionality to handle additional demographics.
- Configure retries or dead-letter queues for S3 failures.

---

## License

This project is licensed under the MIT License.
