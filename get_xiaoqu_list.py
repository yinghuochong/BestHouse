# encoding: utf-8
import logging
import time
import random
from config.config import config
from utils.client import get_data
from models.orm import Session
from models.city import City,Community,District

def get_community_list(city_id,offset,district_id,district_name):
    """
    获取小区列表
    """
    url = 'http://app.api.lianjia.com/house/community/search'
    payload = {
        'city_id': city_id,
        'limit_count': '20',
        'district_id':district_id,
        'district_name':district_name,
        'limit_offset': str(offset)
    }
    logging.info('获取小区列表，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    communities = data["list"]
    logging.info('获取小区列表，total_count：{}'.format(total_count))
    return communities,has_more_data,total_count


def main():
    db_session = Session()

    city_id = config.city_id
    #检查是否支持该城市  
    allcities = db_session.query(City).all()
    city = db_session.query(City).filter(City.city_id == city_id).first()
    if not allcities or len(allcities) <= 0:
        logging.error('请先更新城市列表！')    
        return 

    if not city:
        logging.error('不支持该城市 ：{}'.format(city_id))    
        return 

    alldistricts = db_session.query(District).filter(District.city_id == city_id).all()
    if not alldistricts or len(alldistricts) <= 0:
        logging.error('请先更新该城市信息，获取所有行政区！')    
        return 
    #开始抓数据
    logging.info('开始获取小区数据：{}'.format(city.city_name))
    xiaoqu_number = 0
    for district in alldistricts:
        district_id = district.district_id
        district_name = district.district_name
        logging.info('开始获取 {} 的数据========'.format(district_name))
        offset = 0
        has_more_data = True
        while has_more_data:
            time.sleep(random.randint(0,config.request_max_gap))
            communities,has_more_data,total_count = get_community_list(city_id,offset,district_id,district_name)
            if offset == 0:
                xiaoqu_number = xiaoqu_number + total_count
            offset = offset + 20
            for aCommunity in communities:
                community = Community(city_id, aCommunity)    
                db_session.merge(community)
            db_session.commit()
        logging.info('完成获取 {} 的数据=----------'.format(district_name))
    logging.info('小区数据获取完成：{}, 共有 {} 个小区'.format(city.city_name,xiaoqu_number))
    db_session.commit()
    db_session.close()

if __name__ == '__main__':
    main()