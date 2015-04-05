import json
from bson import json_util

def mongoJsonify(func):
	def JSON(*args, **kwargs):
		return json.dumps(func(*args, **kwargs), indent = 4, default = json_util.default)
	return JSON