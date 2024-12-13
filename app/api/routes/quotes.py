from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.models import Prices, Quotes
from app.utils import get_crypto_prices

router = APIRouter(prefix='/quotes', tags=['quotes'])


@router.get('/', response_model=Quotes)
async def get_live_quotes(session: SessionDep):
	quotes = get_crypto_prices()
	
	for token, price in quotes.items():
		price_entry = session.query(Prices).filter(Prices.symbol == token).first()
		
		if price_entry:
			price_entry.price = price
		else:
			price_entry = Prices(symbol=token, price=price)
			session.add(price_entry)
	
	session.commit()
	
	return Quotes(quotes=quotes)
