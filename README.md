# **Voting Eligibility Checker - AWS Lambda**

---

## **Overview**

This project implements a serverless application using AWS Lambda to check if a person is eligible to vote. It takes `name` and `age` as query parameters through an HTTP request and responds with a personalized message indicating whether the person can vote.

---

### **Features**

- **Input Parameters:** Accepts `name` and `age` as query parameters.
- **Dynamic Responses:** Generates personalized eligibility messages.
- **Error Handling:** Validates input and returns appropriate error messages.
- **Serverless and Scalable:** Uses AWS Lambda for scalable, cost-efficient deployment.

---

### **Technologies**

- **AWS Lambda:** Serverless compute service.
- **AWS API Gateway:** Trigger for handling HTTP requests.
- **Python 3.x:** Language for implementing the Lambda function.
- **JSON:** Format for input/output data.

---

### **How It Works**

1. **Input:**  
   - **name** (string): The person's name (e.g., "John"). Default is `"Guest"`.  
   - **age** (integer): The person's age (e.g., 25).  

2. **Logic:**
   - If the `age` is 18 or above, the response indicates the person is eligible to vote.
   - If the `age` is less than 18, the response shows the number of years left until eligibility.
   - If the `age` is invalid or non-numeric, an error message is returned.

3. **Output:**  
   - A JSON object with a `message` field containing the personalized result.

---

### **API Endpoints**

#### HTTP GET Request

**URL:**  
`https://<api-id>.execute-api.<region>.amazonaws.com/default/voting-eligibility-check`

**Query Parameters:**

- `name`: The name of the person (optional, default: "Guest").
- `age`: The age of the person (required).

---

### **Sample Requests and Responses**

#### **1. Eligible to Vote**

**Request:**  
`GET /voting-eligibility-check?name=John&age=20`

**Response:**

```json
{
  "message": "Hello, John! You are eligible to vote in the election."
}
```

---

#### **2. Not Eligible to Vote**

**Request:**  
`GET /voting-eligibility-check?name=Sarah&age=16`

**Response:**

```json
{
  "message": "Hi, Sarah! You are not eligible to vote yet. You need to wait 2 more year(s)."
}
```

---

#### **3. Invalid Age**

**Request:**  
`GET /voting-eligibility-check?name=Paul&age=abc`

**Response:**

```json
{
  "error": "Invalid age. Please provide a numeric value."
}
```

---

### **Deployment Instructions**

#### **1. Set Up AWS Lambda**

1. Open the AWS Lambda Console and create a new function.
2. Choose **Author from scratch** and configure:
   - **Function Name:** `voting-eligibility-check`.
   - **Runtime:** Python 3.x.
3. Add an execution role with basic Lambda permissions.
4. Deploy the Python code in the function editor.

---

#### **2. Add an API Gateway Trigger**

1. Go to the **Function Overview** section in the Lambda console.
2. Click **Add Trigger** and select **API Gateway**.
3. Configure the trigger:
   - API type: `HTTP API`.
   - Security: `Open`.
4. Save and note the generated API Gateway URL.

---

#### **3. Test the Endpoint**

Use a tool like Postman, cURL, or a web browser to make HTTP GET requests to the API Gateway URL.

---

### **Code Explanation**

#### `lambda_handler(event, context)`

The main entry point for the Lambda function.

- **Input:** The `event` object contains query parameters.
- **Output:** Returns a JSON object with a status code and message.

#### **Logic Breakdown:**

1. Extract `name` and `age` from the `queryStringParameters`.
2. Validate `age` as a numeric value.
3. Compute eligibility:
   - If `age >= 18`: Return an eligible message.
   - Else: Calculate and return years left.
4. Handle errors for invalid input.

---

### **Customization**

You can customize the responses by modifying the `message` values in the function.

---

### **Error Handling**

- **Invalid Input:** If `age` is not numeric, the function returns an HTTP 400 response with an error message.
- **Missing Parameters:** Defaults are used for missing `name` and `age`.

---

### **Future Enhancements**

- Add localization for responses in different languages.
- Integrate with a database to log user queries.
- Add authentication for API requests.

---

### **License**

This project is licensed under the MIT License. You are free to use and modify it.

---

Enjoy building your **Serverless Revolution!**
