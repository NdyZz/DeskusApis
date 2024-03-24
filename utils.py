## - Created By NdyZz [ github.com/NdyZz ]
## - Created On 20/3/2024
## - Contact Me on wa.me/6285346923840

import hashlib, time

def generate_visitor_id():
   timestamp = str(time.time())
   md5_hash = hashlib.md5(timestamp.encode()).hexdigest()
   return md5_hash

def generate_cookie(visitor_id):
   timestamp = str(time.time())
   sha1_hash = hashlib.sha1((timestamp + visitor_id).encode()).hexdigest()
   return sha1_hash