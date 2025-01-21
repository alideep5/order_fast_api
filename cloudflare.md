### **Enable Signed URL Access**

1. In the Stream dashboard, select your uploaded video.
2. Under **Security Settings**, enable **"Require Signed URLs"** to restrict public access.
3. This ensures only authorized requests with a signed token can access the video.


### To generate a **signing key** for Cloudflare Stream, follow these steps:

1. **Obtain Your Account ID**:
    - Log in to your Cloudflare dashboard.
    - Navigate to the **Stream** section.
    - Your **Account ID** is displayed on the Stream dashboard.
2. **Create an API Token with Appropriate Permissions**:
    - In the Cloudflare dashboard, click on your profile icon and select **My Profile**.
    - Go to the **API Tokens** tab and click on **Create Token**.
    - Use the **Custom Token** template and grant the following permissions:
        - **Account**: Stream:Edit
    - Specify the account and set the token's TTL (Time To Live) as needed.
    - Create and save the token securely; you'll need it for API requests.
3. **Generate a Signing Key via the API**:
    - Use the following `curl` command to create a signing key:
        
        ```bash
        bash
        CopyEdit
        curl -X POST \
          -H "Authorization: Bearer <API_TOKEN>" \
          -H "Content-Type: application/json" \
          https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/keys
        
        ```
        
        Replace `<API_TOKEN>` with the token you created and `<ACCOUNT_ID>` with your actual account ID.
        
    - A successful response will include the `pem` (Private Key) and `jwk` (JSON Web Key) values:
        
        ```json
        json
        CopyEdit
        {
          "result": {
            "id": "your_key_id",
            "pem": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
            "jwk": { ... }
          },
          "success": true,
          "errors": [],
          "messages": []
        }
        
        ```