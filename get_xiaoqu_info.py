# encoding: utf-8
import logging
import time
import random
from config.config import config
from utils.client import get_data
from models.orm import Session
from models.city import City,Community,CommunityInfo,OldHouse,HistoryRecord,RentHouse


def get_xiaoqu_info(community_id):
    """
    获取小区详细信息
    """
    url = 'http://app.api.lianjia.com/house/community/detailv2part1'
    payload = {
        'community_id': community_id,
    }
    logging.info('开始获取小区详细信息 ：{}'.format(community_id))
    data = get_data(url, payload, method='GET')
    return data

def get_zufang_list(city_id,community_id,offset):
    """
    获取租房列表
    """
    url = 'http://app.api.lianjia.com/house/zufang/searchV2'
    payload = {
        'city_id': city_id,
        'condition': "c"+community_id,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    logging.info('获取小区租房列表，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    communities = {}
    if data.__contains__("list"):
        communities = data["list"]
    logging.info('获取小区租房列表，total_count：{}'.format(total_count))
    return communities,has_more_data,total_count


def get_history_list(city_id,community_id,offset):
    """
    获取历史成交信息
    """
    url = 'http://app.api.lianjia.com/house/chengjiao/search'
    payload = {
        'city_id': city_id,
        'community_id': community_id,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    logging.info('获取小区成交记录，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    records = {}
    if data.__contains__("list"):
        records = data["list"]
    logging.info('获取小区成交记录，total_count：{}'.format(total_count))
    return records,has_more_data,total_count


def get_ershou_list(city_id,community_id,offset):
    """
    获取二手房列表
    """
    url = 'http://app.api.lianjia.com/house/ershoufang/searchv4'
    payload = {
        'city_id': city_id,
        'condition': "c"+community_id,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    logging.info('获取二手房列表，community_id:{} offset：{}'.format(community_id,offset))
    data = get_data(url, payload, method='GET')
    result = {}
    has_more_data = False
    if data.__contains__("list"):
        result = data["list"]
    if data.__contains__("has_more_data"):
        has_more_data = data["has_more_data"] == 1
    return result,has_more_data


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

    allcommunities = db_session.query(Community).filter(City.city_id == city_id).all()
    logging.info('开始按小区抓取，共有小区 ：{}'.format(len(allcommunities))) 
    for aCommunity in allcommunities:
        #处理小区详细信息
        community_id = aCommunity.community_id
        logging.info('开始获取该小区详细信息：{}'.format(community_id))
        data = get_xiaoqu_info(community_id)
        community_info = CommunityInfo(city_id,data)
        db_session.merge(community_info)
        db_session.commit()
        #获取小区二手房信息
        logging.info('开始获取该小区二手房信息：{}'.format(community_id))
        offset = 0
        has_more_data = True
        while has_more_data:
            time.sleep(random.randint(0,3))
            oldhouses,has_more_data = get_ershou_list(city_id,community_id,offset)
            offset = offset + 20
            for aOldhouse in oldhouses:
                oldHouse = OldHouse(city_id, aOldhouse) 
                if oldHouse.house_code and len(oldHouse.house_code)>0:
                    db_session.merge(oldHouse)
            db_session.commit()
        logging.info('完成获取该小区二手房信息：{}'.format(community_id))
        #获取小区成交信息
        logging.info('开始获取该小区历史成交信息：{}'.format(community_id))
        offset = 0
        has_more_data = True
        while has_more_data:
            time.sleep(random.randint(0,3))
            records,has_more_data,total_count = get_history_list(city_id,community_id,offset)
            offset = offset + 20
            for aRecord in records:
                record = HistoryRecord(city_id, aRecord)    
                db_session.merge(record)
            db_session.commit()
        logging.info('完成获取该小区历史成交信息：{}'.format(community_id))
        #获取小区成交信息
        logging.info('开始获取该小区租房信息：{}'.format(community_id))
        offset = 0
        has_more_data = True
        while has_more_data:
            time.sleep(random.randint(0,3))
            rents,has_more_data,total_count = get_zufang_list(city_id,community_id,offset)
            offset = offset + 20
            for aRent in rents:
                rent = RentHouse(city_id, aRent)    
                db_session.merge(rent)
            db_session.commit()
        logging.info('完成获取该小区租房信息：{}'.format(community_id))
    logging.info('小区信息获取完成。。。。。')

if __name__ == '__main__':
    main()