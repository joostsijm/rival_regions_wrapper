"""Work class"""

import re

from bs4 import BeautifulSoup

RESOURCE_DICT = {
    'oil': 'oil',
    'ore': 'ore',
    'yellow': 'gold',
    'uranium': 'uranium',
    'diamond': 'diamond'
}


class Work():
    """Wrapper class for work"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def switch_factory(self, factory_id):
        """Switch factory based on factory_id"""
        response = self.api_wrapper.post('factory/assign',
                                         data={'factory': factory_id})
        return response

    def work(self, amount=1, mentor=0):
        pass

        # TODO GET THE ORDER OF ALL FACTORY TYPES
        # TODO ASSUME GOLD WILL BE ONLY WEIRD TYPE

        """Work at given factory ID. Amount needs to be energy / 10."""
        response = self.api_wrapper.post(f'factory/go/{amount}/{mentor}/')
        soup = BeautifulSoup(response, 'html.parser')

        self.api_wrapper.authentication.client.LOGGER.info(str([i.replace('\t','') for i in soup.stripped_strings]))

        # GOLD MINE OUTPUT
        #  ['IndX GOLD', '▶', 'Gold mine', '—10 E (+9)', 'Working experience: +1 Pt.',
        #  '0 $', 'Exp: +20', 'Total: 6900420', 'Taxes: +0 $ (10%)', 'Total: 5.657.542.880.418 $',
        #  'Work again', 'Auto']

        # OIL MINE OUTPUT 0% WAGE
        # ['IndX Oil', '▶', 'Oil field', '—10 E (+9)', 'Working experience: +1 Pt.', 'Exp: +20',
        # 'Total: 120660', '+714.962 bbl', 'Taxes: +0 $ (10%)', 'Total: 5.591.261.983.800 $', '+79.440 bbl (10%)',
        # 'Total: 8.716.264.048', 'Work again', 'Auto']

        # Current order - Need more research
        # [factory name, hymn symbol, factory type, energy used (+9? what's this?), working experience gained, xp gain,
        # total you have, # total factory gains?, taxes, total region has, total region gains resource, total region has
        # of the resource, work again and auto work buttons]

    def page(self):
        """Get work page"""
        path = 'work'
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')

        factory = soup.select_one('.work_item:nth-child(9)')
        factory_slide = factory.select_one('.factory_slide')
        factory_dict = {
            'id': int(factory_slide['action'].replace('factory/index/', '')),
            'name': factory_slide.text
        }
        factory_owner = factory.select_one('.factory_whose')
        if factory_owner:
            factory_dict['owner_name'] = factory_owner.text
            factory_dict['owner_id'] = factory_owner['action'].replace(
                    'slide/profile/', ''
                )

        level_str = re.search(
                r'level\s\d+', factory.select_one('.work_source_1').text
            )
        if level_str:
            factory_dict['level'] = int(re.sub(
                r'level\s', '', level_str.group(0)
            ))

        string_list = []
        factory_button = soup.select_one(
                    '.work_factory_button'
                )
        if factory_button:
            for string in factory_button.strings:
                string_list.append(string.strip())
            try:
                wage = string_list[2]
                if '%' in wage:
                    factory_dict['wage_type'] = 'procentage'
                    factory_dict['wage'] = float(wage.replace(' %', ''))
            except IndexError:
                pass

        work_page = {
            'factory': factory_dict,
            'work_exp': {},
            'resources_left': {},
        }

        for resource_left in soup.select('span.imp.tip'):
            classses = resource_left.get('class')
            for class_name, resource_name in RESOURCE_DICT.items():
                if class_name in classses:
                    work_page['resources_left'][resource_name] = \
                        float(resource_left.text)
                    break

        for work_exp in soup.select('.work_exp'):
            work_exp_amount = int(re.sub(
                    r'exp: | Pt\.', '', work_exp.text.strip()
                ))
            work_page['work_exp'][work_exp['url']] = work_exp_amount
        return work_page
