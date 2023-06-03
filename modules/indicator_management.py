import os
import requests
import platform

import cachetools.func

from datetime import datetime, timezone
from urllib3 import encode_multipart_formdata

from modules import utils

ENDPOINTS = {
    "username_hint": "https://www.tradingview.com/username_hint/",
    "list_users": "https://www.tradingview.com/pine_perm/list_users/",
    "modify_access": "https://www.tradingview.com/pine_perm/modify_user_expiration/",
    "add_access": "https://www.tradingview.com/pine_perm/add/",
    "remove_access": "https://www.tradingview.com/pine_perm/remove/",
    "signin": "https://www.tradingview.com/accounts/signin/"
}

class IndicatorManagement:
    """
    Initialize IndicatorManagement class
    
    Kwargs:
        username : This is your TradingView username.
        password : This is your TradingView password.
    """
    _cache = utils.InstanceCache(ttl = 300)

    def __init__(self, username: str, password: str):
            
        payload = {'username': username, 'password': password, 'remember': 'on'}
        body, contentType = encode_multipart_formdata(payload)
        userAgent = 'TWAPI/3.0 (' + platform.system() + '; ' + platform.version() + '; ' + platform.release() + ')'
        login_headers = {'origin': 'https://www.tradingview.com', 'User-Agent': userAgent, 'Content-Type': contentType, 'referer': 'https://www.tradingview.com'}
        login = requests.post(
            url = ENDPOINTS["signin"], 
            data = body, 
            headers = login_headers
        )
        cookies = login.cookies.get_dict()
        self.session_id = cookies["sessionid"]

    def __new__(cls, *args, **kwargs):
        instance = cls._cache.get(cls, args)
        if instance is not None:
            return instance

        instance = super().__new__(cls)
        cls._cache.add(instance, args)
        return instance
        
    @classmethod
    def validate_username(self, username: str):
        """
        This function validates a TradingView username by checking if it exists on TradingView.

        Kwargs:
            username : The TradingView username to validate.
        """  
        
        users = requests.get(ENDPOINTS["username_hint"] + "?s=" + username)
        usersList = users.json()
        validUser = False
        verifiedUserName = ''
        for user in usersList:
            if user['username'].lower() == username.lower():
                validUser = True
                verifiedUserName = user['username']
        return {"validuser": validUser, "verifiedUserName": verifiedUserName}
            
    def get_access_details(self, username: str, pine_id: str) -> dict:
        """
        This function retrieves the access details for a specific user and pine script.

        Kwargs: 
            username : This is the username of the TradingView user for whom you want to retrieve access details.
            pine_id  : This is the ID of the Pine script for which you want to retrieve access details.
        """
                
        user_payload = {'pine_id': pine_id, 'username': username}
        user_headers = {'origin': 'https://www.tradingview.com', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'sessionid=' + self.session_id}
        usersResponse = requests.post(
            url = ENDPOINTS['list_users'] + '?limit=10&order_by=-created', 
            headers = user_headers, 
            data = user_payload
        )
        userResponseJson = usersResponse.json()
        users = userResponseJson['results']
        access_details = user_payload
        hasAccess = False
        noExpiration = False
        expiration = str(datetime.now(timezone.utc))
        for user in users:
            if user['username'].lower() == username.lower():
                hasAccess = True
                strExpiration = user.get("expiration")
                if strExpiration is not None:
                    expiration = user['expiration']
                else:
                    noExpiration = True
        
        access_details['hasAccess'] = hasAccess
        access_details['noExpiration'] = noExpiration
        access_details['currentExpiration'] = expiration
        
        return access_details
    
    def add_access(self, access_details: dict, extension_type: str, extension_length: int) -> dict:
        """
        This function adds access for a user to a Pine script.

        Kwargs:
            access_details   : This is a dictionary containing the access details for a user and Pine script. You can obtain this from the get_access_details function.
            extension_type   : This is a string indicating the type of extension you want to add. It can be 'Y' for years, 'M' for months, 'W' for weeks, 'D' for days, or 'L' for lifetime.
            extension_length : This is an integer indicating the length of the extension. For example, if extension_type is 'M' and extension_length is 3, this would add a 3-month extension.
        """
        noExpiration = access_details['noExpiration']
        access_details['expiration'] = access_details['currentExpiration']
        access_details['status'] = 'Not Applied'
        
        if not noExpiration:
            payload = {'pine_id': access_details['pine_id'], 'username_recip': access_details['username']}
            if extension_type != 'L':
                expiration = utils.get_access_extension(
                    current_expiration_date = access_details['currentExpiration'],
                    extension_type = extension_type,
                    extension_length = extension_length
                )
                payload['expiration'] = expiration
                access_details['expiration'] = expiration
            else:
                access_details['noExpiration'] = True
            enpoint_type = 'modify_access' if access_details['hasAccess'] else 'add_access'
            body, contentType = encode_multipart_formdata(payload)
            headers = {'origin': 'https://www.tradingview.com', 'Content-Type': contentType, 'cookie': 'sessionid=' + self.session_id}
            add_access_response = requests.post(
                url = ENDPOINTS[enpoint_type], 
                data = body, 
                headers = headers
            )
            access_details['status'] = 'Success' if (add_access_response.status_code == 200 or add_access_response.status_code == 201) else 'Failure'
            
        return access_details
    
    def remove_access(self, access_details: dict) -> dict:
        """
        This function removes access for a user to a Pine script.

        Kwargs:
            access_details: This is a dictionary containing the access details for a user and Pine script. You can obtain this from the get_access_details function.
        """
        payload = {'pine_id': access_details['pine_id'], 'username_recip': access_details['username']}
        body, contentType = encode_multipart_formdata(payload)
        headers = {'origin': 'https://www.tradingview.com', 'Content-Type': contentType, 'cookie': 'sessionid=' + self.session_id}
        remove_access_response = requests.post(
            url = ENDPOINTS['remove_access'], 
            data = body, 
            headers = headers
        )
        access_details['status'] = 'Success' if (remove_access_response.status_code == 200) else 'Failure'
        
        return access_details
    