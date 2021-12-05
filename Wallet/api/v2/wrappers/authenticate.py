from flask import request
from functools import wraps

def authenticate(f):
	@wraps(f)
	def wrapped_view(**kwargs):
		auth = request.headers.get("Authorization")

		# Validate user information from provider
		#  ...
		#  ...
		playerId = 123456
		
		if not (auth):
			return ({"Message": "Unauthorized"}, 403)

		return f(playerId, **kwargs)

	return wrapped_view