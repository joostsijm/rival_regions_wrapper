"""Work class"""

import re

from bs4 import BeautifulSoup
import logging
LOGGER = logging.getLogger('rival_regions_wrapper.authentication_handler')


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

    # TODO ENERGY
    # def energy(self):
    #    """Get current amount of energy"""
    #    response = self.api_wrapper.get(path)

    def work(self, amount=1, mentor=0):
        """Work at given factory ID. Amount needs to be energy / 10."""
        response = self.api_wrapper.post(f'factory/go/{amount}/{mentor}/')
        soup = BeautifulSoup(response, 'html.parser')
        """if str(soup.select_one('h1').text.replace('\xa0▶','')) == 'You need residency to work in this region ':
            LOGGER.info(str(soup))
            return False
        else:"""
        #factory = str(soup.select_one('h1').text.split('\xa0▶')[0])
        #factory_type = str(soup.select_one('h1').text.split('\xa0▶')[1])
        #income = str(soup.select_one('div.minwidth.imp').select('.work_results2')[-1].
        #             select('span')[-1].text.replace('.', ''))
        #LOGGER.info(str(soup.select_one('div.minwidth.imp').select('.work_results2')))
        LOGGER.info(str([i for i in soup.stripped_strings]))
        #  ['IndX GOLD', '▶', 'Gold mine', '—10 E\t\t\t\t\t\t\t\t\t\t\t (+9)', 'Working experience: +1 Pt.',
        #  '0 $', 'Exp: +20', 'Total: 6900420', 'Taxes: +0 $ (10%)', 'Total: 5.657.542.880.418 $',
        #  'Work again', 'Auto']
        #income = [i.strip("+") for i in income.split(" ")]  # Split units from value and remove sign
        #LOGGER.info(str(income))
        #income[0] = int(income[0])  # Convert first part to an integer, second will be the units

        #worked_info = {
        #    'factory': factory,
        #    'factory_type': factory_type,
        #    'income': income
        #}
#
        return ''# worked_info

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
