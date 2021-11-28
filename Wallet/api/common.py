def authenticateUser(headers):
	if (headers.get("Authorization")):
		# Retrieving user information from provider
		#  ...
		return {
			"player_id": 123456
		}
	else:
		return {}