## - Created By NdyZz [ github.com/NdyZz ]
## - Created On 20/3/2024
## - Contact Me on wa.me/6285346923840

from flask import (
   Flask,
   request,
   jsonify,
   redirect,
   url_for,
   make_response,
   render_template,
   send_from_directory,
   Response,
   send_file,
   render_template_string
)
from flask_caching import Cache
from flask_cors import CORS, cross_origin
import requests, random, time, urllib, traceback, re, urllib3, socket, html, json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import config as conf
import utils, os, threading, glob, base64
from utils import *
from markupsafe import escape
from html import escape
from email_validator import validate_email, EmailNotValidError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"
app.config["TEMPLATES_AUTO_RELOAD"] = conf.AUTO_RELOAD
cache = Cache(app, config={
   "CACHE_TYPE": "simple",
   "CACHE_DEFAULT_TIMEOUT": 3600
})

## handle error
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
def handle_errors(error):
   return redirect(url_for("index"))
   
## scrape
class BingApi:
  def __init__(self, cookie):
    self.cookie = cookie
    self.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Alt-Used': 'www.bing.com',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1',
      'Cookie': f'{cookie}',
      'X-Forwarded-For': f'{random.randint(20, 254)}.{random.randint(0, 254)}.{random.randint(0, 254)}.{random.randint(0, 254)}',
    }

  def create_images(self, prompt, is_slow_mode=True):
    try:
      payload = f'q={requests.utils.quote(prompt)}'
      credits = self.get_credits() or 0

      # Adjust request based on credits and slow mode
      if credits > 0 and not is_slow_mode:
        response = self.send_request(True, payload)
      else:
        response = self.send_request(is_slow_mode, payload)

      if response.status_code == 200:
        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')

        # Check for errors based on specific classes
        error_count = len(soup.find_all('img', class_='gil_err_img rms_img'))
        if not is_slow_mode and credits > 0 and soup.find('div', id='gilen_son').has_attr('class_', 'show_n'):
          raise Exception('Dalle-3 is currently unavailable due to high demand')
        elif (soup.find('div', id='gilen_son').has_attr('class_', 'show_n') or 
              (error_count == 2 and credits > 0 and is_slow_mode)):
          raise Exception('Slow mode is currently unavailable due to high demand')
        elif error_count == 2:
          raise Exception('Invalid cookie')
        elif error_count == 4:
          raise Exception('Prompt has been blocked')
        else:
          raise Exception('Unknown error')

      event_id = response.headers.get('x-eventid')
      return self.retrieve_images(event_id)
    except Exception as e:
      print(f"Error: {e}")
      return None

  def get_credits(self):
    response = requests.get(f'https://www.bing.com/create', headers=self.headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find(id='token_bal').text.strip() if soup.find(id='token_bal') else None

  def send_request(self, is_slow_mode, payload):
    url = f'https://www.bing.com/images/create?{payload}&rt={(3 if is_slow_mode else 4)}'
    try:
      response = requests.post(url, headers=self.headers, allow_redirects=False)
      return response
    except Exception as e:
      print(f"Error in sendRequest: {e}")
      return None

  def retrieve_images(self, event_id):
    while True:
      images_response = requests.get(f'https://www.bing.com/images/create/async/results/1-{event_id}', headers=self.headers)
      if images_response.text.find('"errorMessage":"Pending"') != -1:
        raise Exception('Error occurred')

      results = []

      if images_response.text == '':
        time.sleep(5)
        continue

      soup = BeautifulSoup(images_response.text, 'html.parser')
      for image in soup.find_all('img', class_='mimg'):
        bad_link = image['src']
        good_link = bad_link[:bad_link.find('?')] # Delete the parameters
        results.append(good_link)

      return results

class UrlShorten:
   TINYURL_URL = "http://tinyurl.com/api-create.php"
   ISGD_URL = "https://is.gd/create.php?format=json&url="
   VGD_URL = "https://v.gd/create.php?format=json&url="
   OUO_URL = "https://ouo.io/api/0G4vYlK2?s="
   BITLY_URL = "https://bitly.ws/create.php?url="
   
   headers = {'User-Agent': UserAgent().random}
   
   @staticmethod
   def tinyurl(url_long):
      try:
         url = UrlShorten.TINYURL_URL + "?" + urllib.parse.urlencode({
            "url": url_long
         })
         res = requests.get(url)
         res.raise_for_status()
         short_url = res.text
         return short_url
      except requests.RequestException as e:
         raise Exception(f'TinyURL error: {str(e)}')
   
   @staticmethod
   def isgd(url_long):
      try:
         url = UrlShorten.ISGD_URL + url_long
         res = requests.get(url)
         res.raise_for_status()
         data = res.json()
         return data.get('shorturl', f'Error: {data.get("error", "Unknown error")}')
      except requests.RequestException as e:
         raise Exception(f'is.gd error: {str(e)}')
         
   @staticmethod
   def vgd(url_long):
      try:
         url = UrlShorten.VGD_URL + url_long
         res = requests.get(url)
         res.raise_for_status()
         data = res.json()
         return data.get('shorturl', f'Error: {data.get("error", "Unknown error")}')
      except requests.RequestException as e:
         raise Exception(f'v.gd error: {str(e)}')
         
   @staticmethod
   def ouo(url_long):
      try:
         url = UrlShorten.OUO_URL + url_long
         res = requests.get(url)
         res.raise_for_status()
         soup = BeautifulSoup(res.text, 'html.parser')
         a = soup.prettify().strip()
         return a
      except requests.RequestException as e:
         raise Exception(f'ouo.io error: {str(e)}')
         
   @staticmethod
   def bitly(url_long):
      try:
         url = UrlShorten.BITLY_URL + url_long
         res = requests.get(url)
         res.raise_for_status()
         soup = BeautifulSoup(res.text, 'html.parser')
         a = [
            b.text for b in soup.find_all(
               "div", {
                  "style": "padding-top: 20;text-align: center; background-color: #EFF7FC"
               }
            )[0].find_all("b")
         ]
         return a[1]
      except requests.RequestException as e:
         raise Exception(f'bit.ly error: {str(e)}')

## home and donate
@app.route("/")
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def index():
   visitor_id = generate_visitor_id()
   cookie = generate_cookie(visitor_id)
   current_date = datetime.now()
   expiration_date = current_date + timedelta(days=7)
   response = make_response(render_template("index.jinja2", configs=conf))
   response.set_cookie(
      '_id',
      value=cookie,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   response.set_cookie(
      '_rf',
      value=cookie+visitor_id,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   response.set_cookie(
      '_hm',
      value=cookie+cookie,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   return response

@app.route("/donate")
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def donate():
   visitor_id = generate_visitor_id()
   cookie = generate_cookie(visitor_id)
   current_date = datetime.now()
   expiration_date = current_date + timedelta(days=7)
   response = make_response(render_template("donate.jinja2", configs=conf))
   response.set_cookie(
      '_id',
      value=cookie,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   response.set_cookie(
      '_rf',
      value=cookie+visitor_id,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   response.set_cookie(
      '_do',
      value=cookie+cookie,
      httponly=True,
      expires=expiration_date,
      samesite="None",
      secure=True
   )
   return response

## rest api
@app.route("/api/translate", methods=["GET"])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def translate():
   from_lang = request.args.get("from", "en")
   to_lang = request.args.get("to", "id")
   text = request.args.get("text")
   
   if not text:
      return jsonify({
         "code": 400,
         "message": "parameter text cannot empty"
      })
   
   headers = {
      "User-Agent": UserAgent().random,
      "Referer": "http://translate.google.com/",
      "Origin": "http://translate.google.com/",
   }
   url = f"https://translate.google.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q={text}"
   response = requests.get(url, headers=headers)
   result = response.json()
   
   if result is not None and len(result) > 0 and len(result[0]) > 0:
      translated_text = result[0][0][0]
   else:
      translated_text = "Translation failed"
   
   return jsonify({
      "author": "NdyZz",
      "from": from_lang,
      "to": to_lang,
      "text": text,
      "result": translated_text,
   })

@app.route('/api/bing', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def bing_img():
   try:
      query = request.args.get('query')
      if not query:
         server = f"{request.host_url}api/bing?query=kucing"
         return jsonify({
            'error': 'No URL provided.',
            'endpoint': server,
            'author': 'NdyZz'
         }), 400
      bingApi = BingApi(conf.COOKIE_BING)
      result = bingApi.create_images(query+'. Anime Style ultra, HD Anime Style, 4K Anime Style, Anime Style, High quality, Ultra grapics, HD Cinematic, anime, 4K resolution, HD quality, Ultra CGI, High quality, Ultra grapics, HD Cinematic', False)
      return jsonify({
         'author': 'NdyZz',
         'result': result
      })
   except Exception as e:
      return jsonify({
         'author': 'NdyZz',
         'error': e
      }), 500

@app.route('/api/simi', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def simsimi():
   try:
      text = request.args.get('text')
      if not text:
         server = f"{request.host_url}api/simi?text=halo"
         return jsonify({
            'error': 'No URL provided.',
            'endpoint': server,
            'author': 'NdyZz'
         }), 400
      headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
         'Accept': 'application/json, text/javascript, */*; q=0.01',
         'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'X-Requested-With': 'XMLHttpRequest',
         'Origin': 'https://simsimi.vn',
         'Alt-Used': 'simsimi.vn',
         'Connection': 'keep-alive',
         'Referer': 'https://simsimi.vn/',
         'Sec-Fetch-Dest': 'empty',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Site': 'same-origin',
      }
      data = {
         'text': text,
         'lc': 'id',
      }
      response = requests.post('https://simsimi.vn/web/simtalk', headers=headers, data=data)
      success = response.json().get('success')
      if success:
         return jsonify({
            'author': 'NdyZz',
            'result': success
         })
      else:
         return jsonify({
            'error': 'requests error',
            'author': 'NdyZz'
         }), 400
   except Exception as e:
      traceback.print_exc()
      print(e)
      return jsonify({'error': str(e)}), 500

@app.route('/api/simi', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def simsimi():
   try:
      text = request.args.get('text')
      if not text:
         server = f"{request.host_url}api/simi?text=halo"
         return jsonify({
            'error': 'No URL provided.',
            'endpoint': server,
            'author': 'NdyZz'
         }), 400
      headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
         'Accept': 'application/json, text/javascript, */*; q=0.01',
         'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'X-Requested-With': 'XMLHttpRequest',
         'Origin': 'https://simsimi.vn',
         'Alt-Used': 'simsimi.vn',
         'Connection': 'keep-alive',
         'Referer': 'https://simsimi.vn/',
         'Sec-Fetch-Dest': 'empty',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Site': 'same-origin',
      }
      data = {
         'text': text,
         'lc': 'id',
      }
      response = requests.post('https://simsimi.vn/web/simtalk', headers=headers, data=data)
      success = response.json().get('success')
      if success:
         return jsonify({
            'author': 'NdyZz',
            'result': success
         })
      else:
         return jsonify({
            'error': 'requests error',
            'author': 'NdyZz'
         }), 400
   except Exception as e:
      traceback.print_exc()
      print(e)
      return jsonify({'error': str(e)}), 500

@app.route('/api/scrapeweb', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def scrap_web():
   try:
      url = request.args.get('url')
      url_base = 'https://api.webscraping.ai/text'
      params = {
         'api_key': "404a63cb-91e8-4e6d-8700-542cff2b46ab",
         'url': url,
         'proxy': 'residential',
         'text_format': 'xml'
      }
      response = requests.get(url_base, params=params)
      data = response.text
      return jsonify({
         'author': 'NdyZz',
         'result': data
      })
   except Exception as e:
      print(str(e))
      return jsonify({'error': str(e)}), 500

@app.route('/api/questionsite', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def question_web():
   try:
      url = request.args.get('url')
      quest = request.args.get('q')
      url_base = 'https://api.webscraping.ai/ai/question'
      params = {
         'api_key': '404a63cb-91e8-4e6d-8700-542cff2b46ab',
         'url': url,
         'proxy': 'residential',
         'question': quest
      }
      response = requests.get(url_base, params=params)
      data = response.text
      return jsonify({
         'author': 'NdyZz',
         'result': data
      })
   except Exception as e:
      print(str(e))
      return jsonify({'error': str(e)}), 500

@app.route('/api/short', methods=['GET'])
@cross_origin()
@cache.cached(timeout=3600, query_string=True)
def shorten_url():
   try:
      url_long = request.args.get('url')
      if not url_long:
         server = f"{request.host_url}api/short?url=URL_LONG"
         return jsonify({
            'error': 'No URL provided.',
            'endpoint': server,
            'author': 'NdyZz'
         }), 400
      if not url_long.startswith('http://') and not url_long.startswith('https://'):
         if request.is_secure:
            url_long = 'https://' + url_long
         else:
            url_long = 'http://' + url_long
      response = {
         'author': 'NdyZz',
         'tinyurl': None,
         'isgd': None,
         'vgd': None,
         'ouo': None,
         'bitly': None,
         'a_status': requests.get(url_long).status_code
      }
      
      try:
         response['tinyurl'] = UrlShorten.tinyurl(url_long)
      except Exception as e:
         response['tinyurl'] = str(e)
         
      try:
         response['isgd'] = UrlShorten.isgd(url_long)
      except Exception as e:
         response['isgd'] = str(e)
         
      try:
         response['vgd'] = UrlShorten.vgd(url_long)
      except Exception as e:
         response['vgd'] = str(e)
      
      try:
         response['ouo'] = UrlShorten.ouo(url_long)
      except Exception as e:
         response['ouo'] = str(e)
         
      try:
         response['bitly'] = UrlShorten.bitly(url_long)
      except Exception as e:
         response['bitly'] = str(e)
      
      return jsonify(response), 200
   except Exception as e:
      traceback.print_exc()
      return jsonify({'error': str(e)}), 500
