# Introduction
Dummy-Web-API is a simple Web API done in Flask with MongoDB and JWT Authentication. Its goal is to
introduce to frontend developers basic API functionalities and to challenge myself to learn new frameworks
and tools. Any feature you wish to see, just ask and I'll implement it eventually.

# Requirements
- Python 3.10.4 or above;
- MongoDBCompass;
- VS Code.

# Getting Started Locally:
Create a ```config.yaml``` and place it in the project root folder:
```yaml
database:
  url: "{mongo local connection url}"
secret_key: "{jwt secret key}"
```
On the VS Code, go to the ```startup.py``` file and press F5 to start debugging, then open a browser
of your choice and access ```http://127.0.0.1:5000/api/``` to view the Swagger documentation.

Happy Codding! 😄

