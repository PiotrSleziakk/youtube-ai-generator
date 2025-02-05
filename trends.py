from pytrends.request import TrendReq

def get_google_trends():
    pytrends = TrendReq(hl='pl-PL', tz=360)
    trends = pytrends.trending_searches(pn='poland')  # Trendy dla Polski
    return trends.head(5).values.tolist()

# Przykład: zwraca listę 5 trendów
trends = get_google_trends()