## - Created By NdyZz [ github.com/NdyZz ]
## - Created On 20/3/2024
## - Contact Me on wa.me/6285346923840

import markdown

PORT = 8000
DEBUG = False
AUTO_RELOAD = True
COOKIE_BING = 'GI_FRE_COOKIE=gi_fre=2; _C_Auth=; MUID=180833C37F84648128EB27857ED26542; _EDGE_V=1; MUIDB=180833C37F84648128EB27857ED26542; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=817651318B8C4EF581E660496F97E1D9&dmnchg=1; _UR=cdxcls=0&QS=0&TQS=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wMy0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyLCJUb2JuIjowfQ==; _clck=y2028h%7C2%7Cfk6%7C0%7C1538; SRCHUSR=DOB=20240318&POEX=W; ANON=A=623619BA690FA0FFF2295AE2FFFFFFFF&E=1d8a&W=1; PPLState=1; KievRPSSecAuth=FACqBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACOxfP63n6HdRaARGLxEVIksUSoG8RuEUwUUJ4UrwiY+Ao3auwSNVVG92ydElXRvNg+VLRLNkvQYsU5QZuEDupsbZW+w1TqSsjfq9rdXcr+VrVbRWRzUhUWyRO5n/FF5nKfoNP2L2hNJBdRRC2e78TLQ39qHWf1RDJV4BA5tld1UynaQeOh0qisbazwY7EPf7wN9b+YHSmJhFkN5GSxUgX5PmA9taxymCLDWplFPIe9NyO7AyUNvfj3F8r7m0iFMgJwYYnKBZ/6dx4tkOY6qI6f1R0LqvRlOA2OyiPImHizIvcKIObUhZSQ1J8HHOjWB2rUt5tW1ZvWeF6WoGKNi1kJ4Cmv91+jz/asuOgBMMh6gtfu2CeuWdikWEXfoI+63T1ICu6Gt3+XbzLf+XgvENkMh7zaLSFqBVSUqUDVoVRBGVjA2gmdCShn7941jfKmLBWodS8O9BV3p47seiZwZJkQm1HpHCZFnrT6dRzZFDkEOBcZGCHssO5kE2RbFQba1xDLJrzuGGHZSjU/gyzwJWcUWe3M7i+zdKSGEJCS0+QPLvWAP7ZoRdDzlWN+hFDGzozV0QShpZ5OqNlZ7gjwTGFP1ZGExCB1lHB5LU4ea8vGD2wPgUKAF0uExs929L9gDg023zGrE+XuQjuBYtDcM6lq8SXohUCFaNll98YAD/7WcRTOgDRzjgF9OPFW+lLm5HYzfZEeHJJ/5ynttEMcwlV5gEM/bYP35hpN+jwCS8o21xS5eU6DLRSbjDNDTz4hmL9o9R7ZliKueX4/bPktve+t6StLjabmu5q8C7vRR4fKdNJM6lsiHtLS1KYliuDqVsvMnZpvDEPxhm69XhBqiS3puuiPm3MVJ+l+qCqL1KYUJrx0pDpfb5fPBkoLmdKZHHRBZE6/Bhu8rMlfXfVNVpzxw7J6bvcqAt3mt9RiI0YdXRz15w3c5Cv7J77ELNmuP6yIZWTfTH4HFKefB3VcUEf3aFOtAAws0WpBkiGd+om0p9UlemJyqKKTRqqsbAzn5hgnBAgMMsZvFwAUov2qhL0MO8mrYCN+4rqJDJNq5TlWRx1q0BqYkW7tC2cbjmi+Q6VbzyfjvqV4KT3NgNaIxfzTvgOcZtNNoem9OeLcBrBX72D05hvC0yKPeP6MLkfCWtkbXVtNAhsz3JfoAWo8tXcqWQILQfR8BNkUsQKB9ZY9JxO2NL1UqmY5f4lFnGdJO35u6yj1e3+3/IeDjXTXJyWKt14ZQbfDMXkIv8f9VPFMOJ1Zt79tcSManywcU3PxnqhET75RsvOIX7SACTeBm/axXayWUq39NQ/ZaipYyNsjSzhZEFOsxbPk/srwc0top8HKHDwmMVwyUmh7AUkSmufrbNb55sPenIS1Q8Ryqn0DyYDZjti2jpcONglsZXaP2PkBv3bs9vTSOND+758c9UJpgbN3zf7bJvqqDwS8H36Mxpz5k6vU3YZKazuzh+/SGx9CNG28tJYJGeQcJh+supWhldB2CcegIsBEIEqxJ+1katB7UUACNb5P2UlLRprbz3LmugNO6BQUfS; _U=13POoSzCb6VYeH5AABdQxCAk8jxZazcLs0eQQNh1ByoZ4hdgEVqXDTweb_RArZbqHiNoVv0vHHNVFUcBh_T25wiH6acEIiQvjgBVQ_Ugl9ROkmZisnnawEFABATBOFH72Jq0RwIvVD57qvHOtiCXNEXA4tm0wFq-Lh3w9h5qeyb1z8Z7D2iT4KdtwbAaKIfjloUEhp2BQs1SsCM9im3ZRKrkc5l2hj0SYUkc7oAFoZGw; WLID=Q9RIC8cARTK+yHFrh+FUM6zBbzNCmPi5iZalMBk9xje5aV0A6PphduFOBSK1aU0rFiCE+3uQD0Y2vSPgxpS9DURZJCqQxNjcuw3lqJNFSYE=; _RwBf=mta=0&rc=0&rb=0&gb=0&rg=0&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=1&l=2024-03-18T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&rwflt=0001-01-01T16:00:00.0000000-08:00&o=0&p=MSAAUTOENROLL&c=MR000T&t=1500&s=2024-03-18T21:19:24.0480915+00:00&ts=2024-03-18T21:19:24.4010990+00:00&rwred=0&wls=2&wlb=0&wle=1&ccp=0&lka=0&lkt=0&aad=0&TH=&e=8hcRf8yHTof3LwnNdEMKtZtZvyOCkFLLlJahdCLIQWyCwyyHTMTIhljSY6WGAffGrqN10uC0G-jUMPKXQQjY9A&A=623619BA690FA0FFF2295AE2FFFFFFFF; _EDGE_S=SID=2DD4435799176E9E05AB571A98526F38; WLS=C=f49b71489f08232e&N=sandi; _SS=SID=2DD4435799176E9E05AB571A98526F38; _C_ETH=1; SRCHHPGUSR=SRCHLANG=id&IG=A14FDDA011D34F5180F4153AAE062A4E&CW=471&CH=943&SCW=471&SCH=943&BRW=MW&BRH=MT&DPR=1.5&UTC=480&DM=0&PV=10.0.0&HV=1710798747&HBOPEN=2&PRVCW=471&PRVCH=435&WTS=63846393353'

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
      "description": "083133318509",
   },
   {
      "image": "./static/images/gopay.png",
      "link": {
         "href": False,
         "text": "Gopay",
      },
      "description": "083133318509",
   },
   {
      "image": "./static/images/ovo.png",
      "link": {
         "href": False,
         "text": "Ovo",
      },
      "description": "083133318509",
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
   },
   {
      "name": "Bing-Image",
      "description": "Parameter untuk membuat gambar dari query/text",
      "parameters": [
         {
            "name": "query",
            "type": "string",
            "required": True
         }
      ],
      "url": "/api/bing?query=kucing"
   }
]
