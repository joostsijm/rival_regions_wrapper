def create_article(
        self,
        title,
        article,
        article_lang="nl",
        paper_id=0,
        category='0',
        region="4001"
):
    """Create new article"""
    self.session.get('http://rivalregions.com/#overview')
    response = self.session.post("http://rivalregions.com/news/post", data={
        'c': self.var_c,
        'newspaper': paper_id,
        'category': category,
        'paper': article,
        'title': title,
        'region': region
    })

def market_info(self, resource, r_id=False):
    """
    Returns a list of data about current resource market state.
    In form price, amount selling, player id, player name string, total offers on market.
    """

    if not r_id:
        res_id = self.resource_id[resource]
    else:
        res_id = resource
    response = self.session.get(f'http://rivalregions.com/storage/market/{res_id}')
    return self.parse_market_response(response, res_id)

def get_all_market_info(self):
    """Request all market info"""
    session = sessions.FuturesSession(session=self.session)
    results = {}
    for type_ in self.resource_id:
        if type_ == 'energy drink':
            continue
        results[type_] = session.get(
            f'http://rivalregions.com/storage/market/{self.resource_id[type_]}?{self.var_c}'
        )
    for res in results:
        result = results[res].result()
        price, selling_amount, player_id, player_name, total_offers = \
            self.parse_market_response(result, self.resource_id[res])
        results[res] = {
            'price': price,
            'amount': selling_amount,
            'player_id': player_id,
            'player_name': player_name,
            'total_offers':total_offers
        }
    return results

@staticmethod
def parse_market_response(response, res_id):
    """Parse market response"""
    price = re.search('<input price="(.*)" type', response.text).group(1)
    selling_amount = re.search('<span max="(.*)" url="', response.text).group(1)
    player_id = re.search(
        '<span action="slide/profile/(.*)" class="storage_see pointer dot hov2', response.text
    ).group(1)
    player_name = re.search(
        f'<span action="slide/profile/{player_id}" class="storage_see pointer dot hov2">(.*)</span>',
        response.text
    ).group(1)
    total_offers = re.search(
        f'Best offer out of <span action="storage/listed/{res_id}" class="storage_see pointer hov2"><span class="dot">(.*)</span></span>:',
        response.text
    ).group(1)
    return price, selling_amount, player_id, player_name, total_offers
