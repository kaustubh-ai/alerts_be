import json
import time

import requests

from app.constants import TOKENS
from app.core.config import settings
from app.core.models import Alert, Prices


def get_crypto_prices():
	url = f'{settings.CRYPTO_URL}/cryptocurrency/quotes/latest'
	parameters = {'symbol': ','.join(TOKENS)}
	headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': settings.CRYPTO_API_KEY}
	res = requests.get(url, params=parameters, headers=headers)
	data = res.json()
	
	# with open('quotes.json', 'w') as f:
	# 	json.dump(data, f, indent=2)
	
	# with open('quotes.json', 'r') as f:
	# 	data = json.load(f)
	
	return {token: round(data['data'][token][0]['quote']['USD']['price'], 4)
	        for token in TOKENS if token in data['data']}


def load_template(template, to_replace=None):
	content = '<div><b>You price alert has been triggered for [token] at [price]</b></div>'
	
	if to_replace:
		for key, value in to_replace.items():
			content = content.replace(key, str(value))
	
	return content


def get_payload(email_to, email_subject, to_replace):
	payload = {'from': {'address': 'noreply@stockemy.in'},
	           'to': [{'email_address': {'address': email_to, 'name': 'Support'}}],
	           'subject': email_subject,
	           'htmlbody': load_template('alert', to_replace)}
	
	return json.dumps(payload)


def send_email(url, email_to, token, price):
	payload = get_payload(email_to, 'Price Alert', {'[token]': token, '[price]': price})
	res = requests.request('POST', url, data=payload,
	                       headers={'authorization': f'Zoho-enczapikey {settings.ZOHO_TOKEN}'})
	
	return res


def monitor_alerts():
	from sqlmodel import Session, select
	from app.core.db import engine
	
	while True:
		with Session(engine) as sess:
			live_prices = get_crypto_prices()
			past_prices = {price.symbol: price.price for price in sess.exec(select(Prices)).all()}
			alerts = sess.exec(select(Alert)).all()
			
			for alert in alerts:
				alert_id, token, price, condition, email = alert.alert_id, alert.token, alert.price, alert.condition, alert.created_by
				live_token_price, past_token_price = live_prices.get(token), past_prices.get(token)
				
				if (condition == 'above' and past_token_price < price < live_token_price) or \
				   (condition == 'below' and past_token_price > price > live_token_price):
					send_email(settings.EMAIL_URL, email, token, price)
			
			print(f'Alerts checked at {time.ctime()} for {len(alerts)} alerts and {len(past_prices)} tokens from db')
		
		time.sleep(10)
