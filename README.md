# API Endpoints
<h4><u>GET indicator_manager/access_details/{username}</u></h4>
Stuff
<br></br>

<h4><u>POST indicator_manager/add</u></h4>
<b>Headers</b>

```json
{
    "TRADINGVIEW-USERNAME": "",
    "TRADINGVIEW-PASSWORD": ""
}
```

**Payload**
```jsonc
{
    "username": "",
    "pine_id": "",
    "extension_type": "",
    "extension_length": "" // Ignored if 'extension_type' == 'L'
}
```

<h4><u>POST indicator_manager/remove</u></h4>
<b>Headers</b>

```json
{
    "TRADINGVIEW-USERNAME": "",
    "TRADINGVIEW-PASSWORD": ""
}
```

**Payload**
```jsonc
{
    "username": "",
    "pine_id": "",
    "extension_type": "",
    "extension_length": "" // Ignored if 'extension_type' == 'L'
}
```

<h4><u>GET indicator_manager/validate/{username}</u></h4>

Can be used to validate username. This can be handy operation to execute before trying to execute access management for the user. If user is not valid, we can stop the workflow then and there.


# Methods
<i>`modules.indicator_management.IndicatorManagement.__init__()`</i>

Initialize IndicatorManagement class
```
Kwargs:
    username : This is your TradingView username. You'll need this to log into TradingView if the provided session ID is not valid.
    password : This is your TradingView password. You'll need this to log into TradingView if the provided session ID is not valid.
```

---

<i>`modules.indicator_management.IndicatorManagement.get_access_details()`</i>

This function retrieves the access details for a specific user and pine script.
```
Kwargs: 
    username : This is the username of the TradingView user for whom you want to retrieve access details.
    pine_id  : This is the ID of the Pine script for which you want to retrieve access details.
```

---

<i>`modules.indicator_management.IndicatorManagement.add_access()`</i>

This function adds access for a user to a Pine script.
```
Kwargs:
    access_details   : This is a dictionary containing the access details for a user and Pine script. You can obtain this from the get_access_details function.
    extension_type   : This is a string indicating the type of extension you want to add. It can be 'Y' for years, 'M' for months, 'W' for weeks, 'D' for days, or 'L' for lifetime.
    extension_length : This is an integer indicating the length of the extension. For example, if extension_type is 'M' and extension_length is 3, this would add a 3-month extension.
```

---

<i>`modules.indicator_management.IndicatorManagement.remove_access()`</i>

This function removes access for a user to a Pine script.
```
Kwargs:
    access_details: This is a dictionary containing the access details for a user and Pine script. You can obtain this from the get_access_details function.
```

---

<i>`modules.indicator_management.IndicatorManagement.validate_username()`</i>

This function validates a TradingView username by checking if it exists on TradingView.
```
Kwargs:
    username : The TradingView username to validate.
```

# Response examples
<i>`modules.indicator_management.IndicatorManagement.get_access_details()`</i>
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":false,
	"noExpiration":false,
	"currentExpiration":"2023-06-02 00:11:55.976542+00:00"
}
```

If the user is whitelisted, the response is as shown below.
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":true,
	"noExpiration":false,
	"currentExpiration":"2023-06-03T00:11:55.976542+00:00"
}
```

<i>`modules.indicator_management.IndicatorManagement.add_access()`</i>
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":false,
	"noExpiration":false,
	"currentExpiration":"2023-06-02 00:11:55.976542+00:00",
	"expiration":"2023-06-03 00:11:55.976542+00:00",
	"status":"Success"
}
```

If the user is whitelisted, the response is as shown below.
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":true,
	"noExpiration":false,
	"currentExpiration":"2023-06-03T00:11:55.976542+00:00",
	"expiration":"2023-06-04 00:11:55.976542+00:00",
	"status":"Success"
}
```

<i>`modules.indicator_management.IndicatorManagement.remove_access()`</i>
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":true,
	"noExpiration":false,
	"currentExpiration":"2023-06-04T00:11:55.976542+00:00",
	"status":"Success"
}
```

If the user isn't whitelisted, the response is as shown below.
```json
{
	"pine_id":"PUB;1f7c1407d82a4a32bff39c1c9a38a290",
	"username":"chutireality",
	"hasAccess":false,
	"noExpiration":false,
	"currentExpiration":"2023-06-02 00:14:39.245333+00:00",
	"status":"Success"
}
```

<i>`modules.indicator_management.IndicatorManagement.validate_username()`</i>
```json
{
	"validuser":true,
	"verifiedUserName":"Chuti"
}
```

If you pass an invalid user, the response is as shown below.
```json
{
	"validuser":false,
	"verifiedUserName":""
}
```