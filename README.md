# Response examples
`modules.indicator_management.get_access_details()`
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

`modules.indicator_management.add_access()`
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

`modules.indicator_management.remove_access()`
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
If the user is whitelisted, the response is as shown below.
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

`modules.indicator_management.validate_username()`
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