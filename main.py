## - Created By NdyZz [ github.com/NdyZz ]
## - Created On 20/3/2024
## - Contact Me on wa.me/6285346923840

import config as conf
from routes import app
from threading import Thread

def run_flask():
   app.run(debug=conf.DEBUG, port=conf.PORT, host="0.0.0.0")

@app.after_request
def add_header(response):
   response.headers['Connection'] = 'keep-alive'
   return response

if __name__ == "__main__":
   run_flask()
