import flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True
import boto3
import botocore

client = boto3.client('cloudformation',region_name = "",aws_access_key_id="",
        aws_secret_access_key="")

@app.route('/', methods=['GET'])
def home():
    return render_template('./index.html')

@app.route('/stack', methods=['GET'])
def stack():
    return render_template('./stack.html')

@app.route('/data', methods=['POST'])
def data():
    try:
        
        f = open('awstemplate.json',) 
        data = json.load(f) 
        stackname=request.form["sname"]
        data["Parameters"]["InstanceType"]["Default"] = request.form["instancetype"]
        data["Parameters"]["KeyName"]["Default"] = request.form["keypair"]
        data["Parameters"]["SSHLocation"]["Default"] = request.form["sshlocation"]
        data["Parameters"]["DBName"]["Default"] = request.form["dbname"]
        data["Parameters"]["DBUser"]["Default"] = request.form["dbuser"]
        data["Parameters"]["DBPassword"]["Default"] = request.form["dbpassword"]
        data["Parameters"]["DBRootPassword"]["Default"] = request.form["dbrootpassword"]
        response = client.create_stack(
        StackName=request.form["sname"],
        TemplateBody= json.dumps(data),
        )
        print(response)
        
    except botocore.exceptions.ParamValidationError as param_error:
        print(param_error)
    return redirect(url_for('stack'))

@app.route('/stack-information', methods=['POST'])
def stackinfo():
    response = client.describe_stacks()
 

    return response

app.run()