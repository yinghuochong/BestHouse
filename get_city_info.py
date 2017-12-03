import logging
from config.config import config
from utils.client import get_data
from models.orm import Session
from models.city import District,Subway

def get_city_info(city_id):
    """
    获取城市信息
    """
    url = 'http://app.api.lianjia.com/config/config/initData'

    payload = {
        'params': '{{"city_id": {}, "mobile_type": "android", "version": "8.0.1"}}'.format(city_id),
        'fields': '{ "city_info": "", "city_config_all": ""}'
    }
    logging.info('开始获取城市信息')
    data = get_data(url, payload, method='POST')
    isFind = False
    for a_city in data['city_config_all']['list']:
        if a_city['city_id'] == city_id:
            isFind = True
            break
    if not isFind:
      logging.info('链家暂未收录该城市：{}'.format(city_id))
      return 
    city_info = data['city_info']['info'][0]
    subway_lines = city_info["subway_line"]
    districts = city_info["district"]

    db_session = Session()
    for aSubway in subway_lines:
        subway = Subway(city_id, aSubway)
        db_session.merge(subway)
    for aDistrict in districts:
        district = District(city_id, aDistrict)
        db_session.merge(district)
    db_session.commit()
    db_session.close()
    logging.info('城市信息更新完成：{}'.format(city_id))


def main():
  city_id = config.city_id
  get_city_info(city_id)


if __name__ == '__main__':
    main()