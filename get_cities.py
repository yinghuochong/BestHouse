import logging
from config.config import config
from utils.client import get_data
from models.orm import Session
from models.city import City

def get_city_list():
    """
    获取城市列表
    """
    url = 'http://app.api.lianjia.com/config/config/initData'

    payload = {
        'params': '{{"city_id": {}, "mobile_type": "android", "version": "8.0.1"}}'.format('110000'),
        'fields': '{ "city_config_all": ""}'
    }
    logging.info('开始更新城市列表')
    data = get_data(url, payload, method='POST')
    db_session = Session()
    for a_city in data['city_config_all']['list']:
        city = City(a_city)
        db_session.merge(city)
    db_session.commit()
    db_session.close()
    logging.info('城市列表更新完成，数据表名称：{}'.format(City.__tablename__))

def main():
  get_city_list()


if __name__ == '__main__':
    main()