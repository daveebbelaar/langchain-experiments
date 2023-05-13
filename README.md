# Deploy Your Slack AI Bot to Azure

## 1. Introduction

Welcome to this tutorial on deploying your Python-based Slack bot to an Azure Web App! In the previous video, we built a Slack bot locally and tested it using ngrok. In this tutorial, we will take it a step further and deploy the bot to the cloud using Azure, allowing it to be accessible from anywhere. Although we are using Azure in this tutorial, you can achieve similar results using other cloud platforms, such as AWS or Google Cloud Platform.

By the end of this tutorial, you will learn how to:

- Set up an Azure account and deploy a web app using the Deployment Center.
- Update the GitHub Actions workflow file to enable automated deployments.
- Update the Python file to allow running on Azure and implement Slack verification.
- Update the Slack App Event Subscription with the new Azure URL.

Understanding how to deploy apps is incredibly valuable as it enables you to deliver end-to-end solutions for your projects. By understanding the entire process, from development to deployment, you can bypass the need for multiple specialized teams and make a more significant impact on your projects. End-to-end solutions mean that you are capable of taking an idea from conception to completion, ensuring seamless integration and smooth operation. This skill allows you to stand out by bridging the gap between data science and software engineering, and I find that it is often overlooked in online tutorials.

## 2. Azure Setup

In this section, we will guide you through setting up an Azure account and deploying a web app using the Deployment Center. Azure provides a comprehensive platform for deploying and managing your applications in the cloud.

Follow these steps to set up your Azure account and deploy your Slack bot:

1. **Sign up for an Azure account**: If you don't already have an account, sign up for a free Azure account at https://azure.microsoft.com. New users are eligible for a $200 credit, which you can use to explore and experiment with Azure services.

2. **Create a Resource Grou**p: A resource group helps you organize and manage resources based on their lifecycle and their relationship to each other. In the Azure Portal, create a new resource group called `LangChain-Experiments`.

3. **Create an App Service**: An App Service is a fully managed platform for building, deploying, and scaling your web apps. In the Azure Portal, create a new App Service and associate it with the `LangChain-Experiments` resource group. Set publish to `Code`, and select the correct `Python` version and your `Region`. Finally, select an appropriate App Service Plan based on your needs. There is a free plan available.

4. **Deploy via GitHub repo**: In the Azure Deployment Center, connect your GitHub repository to your App Service. This will enable continuous integration and deployment, so your app will be automatically updated whenever you push changes to the specified branch. Make sure to select the correct branch.

Once you've completed these steps, your Azure account will be set up and ready for deploying your Slack bot. In the next sections, we will discuss how to update the workflow file, the Python file, and the Slack App Event Subscription to complete the deployment process.

### 2.1 Create a startup.txt file

Create a `startup.txt` file in the root of your project with the following content. This file will be used to configure Gunicorn as the application server for your Flask app when deployed to Azure.

```bash
gunicorn --bind=0.0.0.0 --timeout 600 --chdir slack app:flask_app
```

### 2.2 Update the Startup Command in Azure

In the Azure portal, navigate to your App Service, and then go to Configuration > General Settings. Under the "Startup command" field, enter the following command and click "Save" to apply the changes.
```
startup.txt
```

### 2.3 Update the Web App Configuration with Keys and Secrets

In the Azure portal, navigate to your App Service, and then go to Configuration > Application settings. Add the following keys and their respective values. Make sure to replace the placeholder values with your actual keys and secrets. Click "Save" to apply the changes.

- `OPENAI_API_KEY`: Your OpenAI API key
- `SLACK_BOT_TOKEN`: Your Slack bot token (starts with "xoxb-")
- `SLACK_BOT_USER_ID`: Your Slack bot user ID
- `SLACK_SIGNING_SECRET`: Your Slack signing secret


## 3. Updating the Workflow File

In this section, we'll go over updating the GitHub Actions workflow file to enable automated deployments to your Azure App Service. We'll configure the workflow to log in to Azure CLI using a service principal and update the Azure credentials in GitHub Actions secrets.

Follow these steps to update the workflow file:

1. **Log in to Azure CLI using service principal**: In your GitHub Actions workflow file, add the following code snippet to enable logging in to the Azure CLI using a service principal:

``` yml
- name: Log in to Azure CLI using service principal
  uses: azure/login@v1
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```

2. **Create the service principal**: To create a service principal, run the following command in the Azure Cloud Shell, replacing `<YOUR-SUBSCRIPTION-ID>` with your actual subscription ID (Home > Subscriptions). This command will output a JSON object containing the necessary credentials, such as `clientId`, `clientSecret`, `subscriptionId`, and `tenantId`.

```bash
az ad sp create-for-rbac --name "mySlackBotApp" --role contributor --scopes /subscriptions/<YOUR-SUBSCRIPTION-ID> --sdk-auth
```

3. **Update Azure credentials in GitHub Actions secrets**: In your GitHub repository, navigate to the "Settings" tab and then click on "Secrets and variables > Actions" in the left sidebar. Create a new repository secret named `AZURE_CREDENTIALS` and paste the JSON object you obtained in the previous step as its value.

With these updates in place, your GitHub Actions workflow is now configured to automatically deploy your Slack bot to Azure whenever you push changes to the specified branch. In the next sections, we will discuss updating the Python file and the Slack App Event Subscription to complete the deployment process.

## 4. Updating the Python File

In this section, we will update the Python file to allow running on Azure and implement Slack verification.

Follow these steps to update the Python file:

1. **Update the Flask app to run on Azure**: Modify the flask_app.run() line in your Python file to ensure that the Flask app listens to all incoming connections on the specified port. This is necessary for running the app on Azure. Update the line as follows:

```python
flask_app.run(host="0.0.0.0", port=8000)
```

2. **Implement Slack verification**: To enhance the security of your Slack bot, you need to verify incoming requests from Slack. Add the following `require_slack_verification()` and `verify_slack_request()` functions to your Python file:

```python

signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def require_slack_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not verify_slack_request():
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def verify_slack_request():
    # Get the request headers
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")

    # Check if the timestamp is within five minutes of the current time
    current_timestamp = int(time.time())
    if abs(current_timestamp - int(timestamp)) > 60 * 5:
        return False

    # Verify the request signature
    return signature_verifier.is_valid(
        body=request.get_data().decode("utf-8"),
        timestamp=timestamp,
        signature=signature,
    )
```

3. **Add the decorators**: Make sure to call this function before processing any requests from Slack to ensure that they are legitimate:

```python
@flask_app.route("/slack/events", methods=["POST"])
@require_slack_verification
def slack_events():
    return handler.handle(request)

```

4. **Deploy**: Commit and push the changes to GitHub to trigger the deployment action. Reference the Azure Log Stream for debugging.

After making these changes, your Python file will be ready to run on Azure, and your Slack bot will have improved security through request verification. In the next section, we will discuss updating the Slack App Event Subscription with the new Azure URL.


## 5. Updating the Slack App Event Subscription

Now that your Slack bot is deployed on Azure, you need to update the Slack App Event Subscription with the new URL. This will ensure that your bot receives events from Slack at the correct endpoint.

Follow these steps to update the Slack App Event Subscription:

1. **Navigate to the Slack App Management page**: Go to https://api.slack.com/apps and sign in with your Slack account. Select the app you created for your Slack bot.

2. **Access the Event Subscriptions settings**: In the left sidebar of your app's management page, click on "Event Subscriptions" to access the settings for this feature.

3. **Enable and update the Request URL**: If you haven't already enabled event subscriptions, toggle the switch to enable it. Update the "Request URL" field with the new Azure URL of your deployed app. The URL should be in the format `https://app-name.azurewebsites.net/slack/events`. Replace `app-name` with the name of your App Service (e.g., slack-gpt-app).

4. **Verify the new Request URL**: After entering the new URL, Slack will send a verification request to the provided endpoint. Make sure that your app verifies the request successfully. If there are any issues, double-check your Azure deployment, the Python code for Slack request verification, and the provided URL.

5. **Save the changes**: Once the new Request URL is verified, click the "Save Changes" button at the bottom of the Event Subscriptions settings page.

With these updates, your Slack App Event Subscription will now send events to your bot deployed on Azure. Your Python-based Slack bot is now fully deployed to the cloud and accessible from anywhere, enabling seamless integration with Slack and improving the overall functionality of your application.




## Datalumina

This document is provided to you by Datalumina. We help data analysts, engineers, and scientists launch and scale a successful freelance business — $100k+ /year, fun projects, happy clients. If you want to learn more about what we do, you can visit our [website](https://www.datalumina.io/) and subscribe to our [newsletter](https://www.datalumina.io/newsletter). Feel free to share this document with your data friends and colleagues.

## Tutorials
For video tutorials on how to use the LangChain library and run experiments, visit the YouTube channel: [youtube.com/@daveebbelaar](youtube.com/@daveebbelaar)

