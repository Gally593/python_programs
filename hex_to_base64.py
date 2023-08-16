import base64

hex_val = 'put_hex_value_here'
print(base64.b64encode(((bytes.fromhex(hex_val)))))


