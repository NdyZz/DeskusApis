## - Created By NdyZz [ github.com/NdyZz ]
## - Created On 20/3/2024
## - Contact Me on wa.me/6285346923840

import markdown

PORT = 8000
DEBUG = False
AUTO_RELOAD = True

# SOCIAL MEDIA LINK :)
SOCIAL_MEDIA = {
   "telegram": "https://t.me/Pysandi",
   "facebook": "https://www.facebook.com/ndyzz004",
   "instagram": "https://www.instagram.com/ndyzz004",
   "github": "https://github.com/NdyZz",
}

APP_TITLE = "DeskusAPIs"
APP_DESCRIPTION = "API ini dibuat untuk memudahkan harimu."

AUTHOR_NAME = "NdyZz"
AUTHOR_LINK = "https://github.com/NdyZz"

CHANGELOG = []

GALERIES = []

DONATE = [
   {
      "image": "./static/images/dana.png",
      "link": {
         "href": False,
         "text": "Dana",
      },
      "description": "085346923840",
   },
   {
      "image": "./static/images/gopay.png",
      "link": {
         "href": False,
         "text": "Gopay",
      },
      "description": "085346923840",
   },
   {
      "image": "./static/images/ovo.png",
      "link": {
         "href": False,
         "text": "Ovo",
      },
      "description": "085346923840",
   }
]

API_SERVICES = [
   {
      "name": "Translate",
      "description": "Parameter untuk menerjemahkan semua bahasa",
      "parameters": [
         {
            "name": "text",
            "type": "string",
            "required": True
         },
         {
            "name": "from",
            "type": "string",
            "required": False
         },
         {
            "name": "to",
            "type": "string",
            "required": False
         }
      ],
      "url": "/api/translate?text=welcome&from=en&to=id"
   },
   {
      "name": "Short Url",
      "description": "Parameter untuk memperpendek url",
      "parameters": [
         {
            "name": "url",
            "type": "string",
            "required": True
         }
      ],
      "url": "/api/short?url=https://github.com/NdyZz"
   }
]
