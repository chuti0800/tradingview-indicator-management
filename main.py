import json
import requests
import traceback

from flask import Flask, request

from modules import utils
from modules.indicator_management import IndicatorManagement

with open(file = "./config.json", mode = "r", encoding = "utf-8") as config_file:
    config = json.load(config_file)

app = Flask(__name__)

@app.route(rule = "/indicator_manager/add", methods = ["POST"])
def add_access():
    try:
        try:
            assert request.headers.get("TRADINGVIEW-USERNAME", None) != None, "You haven't passed the user login credential."
            assert request.headers.get("TRADINGVIEW-PASSWORD", None) != None, "You haven't passed the password login credential."
            assert request.json.get("username", None) != None, f"A username was expected in the JSON."
            assert request.json.get("pine_id", None), f"A 'pine_id' was expected in the JSON."
            assert request.json.get("extension_type", None) in ('L', 'Y', 'M', 'W', 'D'), f"Expected 'L', 'Y', 'M', 'W' or 'D', received {request.json['extension_type']}"
            if request.json["extension_type"] != "L":
                assert isinstance(request.json.get("extension_length", None), int), f"Expected an integer, received type: {type(request.json['extension_length'])} ({request.json['extension_length']})" 
        except AssertionError as assert_error:
            utils.log("warning", f"Error: {assert_error} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
            return json.dumps({'result': False, 'error': str(assert_error)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

        # Initialize IndicatorManagement class
        indicator_management = IndicatorManagement(
            username = request.headers["TRADINGVIEW-USERNAME"],
            password = request.headers["TRADINGVIEW-PASSWORD"]
        )
            
        try:   
            # Validate TradingView username
            #validate_username_result = requests.get(
            #    url = f"{config['Server']['Protocol']}://{config['Server']['IP']}:{config['Server']['Port']}/indicator_manager/validate/{request.json['username']}"
            #)
            validate_username_result = indicator_management.validate_username(
                username = request.json['username']
            )
            utils.log("info", f"URL: {request.url} - IP: {request.remote_addr} - Request: {request.json} - Response: {validate_username_result}")
            if not validate_username_result["validuser"]:
                utils.log("info", f"Message: The provided user is invalid - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
                return json.dumps({'result': False, 'error': "The provided user is invalid."}), 500, {'Content-Type': 'application/json; charset=utf-8'}

            access_details = indicator_management.get_access_details(
                username = request.json["username"], 
                pine_id = request.json["pine_id"]
            )

            add_access_result = indicator_management.add_access(
                access_details = access_details, 
                extension_type = request.json["extension_type"], 
                extension_length = 1 if request.json["extension_type"] == "L" else request.json["extension_length"]
            )
            utils.log("info", f"URL: {request.url} - IP: {request.remote_addr} - Request: {request.json} - Response: {add_access_result}")
            
            response = json.dumps({'result': True, 'response': add_access_result})
            return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
        
        except Exception as error:
            response = json.dumps({'result': False, 'error': str(error)})
            utils.log("warning", f"Error: {str(error)} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
            return json.dumps({'result': False, 'error': str(assert_error)}), 500, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as error:
        utils.log("info", f"Error: {str(error)} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
        return json.dumps({'result': False, 'error': 'There was an unexpected error.'}), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route(rule = "/indicator_manager/validate/<username>", methods = ["GET"])
def validate_username(username: str):
    try:
        assert username != None, f"A username was expected, received {username}"
    except AssertionError as assert_error:
        utils.log("warning", f"Error: {assert_error} - URL: {request.url} - IP: {request.remote_addr}")
        return json.dumps({'result': False, 'error': str(assert_error)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

    try:
        validate_username_result = IndicatorManagement.validate_username(username)
        response = json.dumps({'result': True, 'response': validate_username_result})
        utils.log("info", f"URL: {request.url} - IP: {request.remote_addr} - Response: {response}")
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as error:
        utils.log("warning", f"Error: {str(error)} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
        return json.dumps({'result': False, 'error': str(error)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route(rule = "/indicator_manager/remove", methods = ["POST"])
def remove_access():
    try:
        try:
            assert request.headers.get("TRADINGVIEW-USERNAME", None) != None, "You haven't passed the user login credential."
            assert request.headers.get("TRADINGVIEW-PASSWORD", None) != None, "You haven't passed the password login credential."
            assert request.json.get("username", None) != None, f"A username was expected in the JSON."
            assert request.json.get("pine_id", None), f"A 'pine_id' was expected in the JSON."
        except AssertionError as assert_error:
            utils.log("warning", f"Error: {assert_error} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
            return json.dumps({'result': False, 'error': str(assert_error)}), 500, {'Content-Type': 'application/json; charset=utf-8'}

        # Initialize IndicatorManagement class
        indicator_management = IndicatorManagement(
            username = request.headers["TRADINGVIEW-USERNAME"],
            password = request.headers["TRADINGVIEW-PASSWORD"]
        )
        
        # Get access details
        access_details_result = indicator_management.get_access_details(
            username = request.json["username"],
            pine_id = request.json["pine_id"]
        )
        if not access_details_result["hasAccess"]:
            # User has no access. No need to remove access.
            utils.log("info", f"Message: User has no access. No need to remove access. - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json} - Response: {access_details_result}")
            response = json.dumps({'result': True, 'message': 'User has no access. No need to remove access.', 'response': access_details_result})
            return response, 200, {'Content-Type': 'application/json; charset=utf-8'}

        # Remove access
        remove_access_result = indicator_management.remove_access(
            access_details = access_details_result
        )
        
        utils.log("info", f"URL: {request.url} - IP: {request.remote_addr} - Request: {request.json} - Response: {remove_access_result}")

        response = json.dumps({'result': True, 'response': remove_access_result})
        return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as error:
        utils.log("warning", f"Error: {str(error)} - URL: {request.url} - IP: {request.remote_addr} - Request: {request.json}")
        return json.dumps({'result': False, 'error': 'There was an unexpected error.'}), 500, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(
        host = config["Server"]["IP"],
        port = config["Server"]["Port"]
    )
    