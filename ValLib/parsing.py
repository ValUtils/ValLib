import json
import jwt
import base64
import zlib

from .exceptions import DecodeException

def encode_json( data ):
	str = json.dumps(data).encode("utf-8")
	return base64.b64encode(str).decode("utf-8")

def decode_json( data ):
	str = base64.b64decode(data.encode("utf-8"))
	return json.loads(str)

def magic_decode( string: str ):
	try:
		return json.loads(string)
	except:
		pass
	try:
		return jwt.decode(string, options={"verify_signature": False})
	except:
		pass
	raise DecodeException(string)

def zdecode( b64string ):
	decoded_data = base64.b64decode( b64string )
	return zlib.decompress( decoded_data , -15)

def zencode( string_val ):
	zlibbed_str = zlib.compress( string_val )
	compressed_string = zlibbed_str[2:-4]
	return base64.b64encode( compressed_string )

def zloads( b64string ):
	inflated_data = zdecode(b64string)
	return json.loads(inflated_data)

def zdumps( data ):
	stringify = json.dumps(data).encode("utf-8")
	return zencode(stringify).decode("utf-8")
