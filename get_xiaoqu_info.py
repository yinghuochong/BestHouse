# encoding: utf-8
import logging
import time
import random
from config.config import config
from utils.client import get_data
from models.orm import Session
from models.city import City, Community, CommunityInfo, OldHouse
from models.city import HistoryRecord, RentHouse, District, RentRecord


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

#price_type 为 1-10的数字
def get_zufang_list(city_id, community_id, offset, price_type):
    """
    获取租房列表
    """
    temp_codition = ""
    if price_type > 0:
        temp_codition = "rp" + str(price_type)
    url = 'http://app.api.lianjia.com/house/zufang/searchV2'
    payload = {
        'city_id': city_id,
        'condition': "c" + community_id + temp_codition,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    logging.info('获取小区租房列表，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    rents = {}
    if data.__contains__("list"):
        rents = data["list"]
    logging.info('获取小区租房列表，total_count：{}'.format(total_count))
    return rents, has_more_data, total_count

#price_type 为 1-10的数字
def get_zufang_history(city_id, community_id, offset, price_type):
    """
    获取租房成交列表
    """

    temp_codition = ""
    if price_type > 0:
        temp_codition = "rp" + str(price_type)
    url = 'http://app.api.lianjia.com/house/rented/search'
    payload = {
        'city_id': city_id,
        'condition': temp_codition + "c" + community_id,
        'community_id': community_id,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    logging.info('获取小区租房成交记录，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    rentRecords = {}
    if data.__contains__("list"):
        rentRecords = data["list"]
    logging.info('获取小区租房成交记录，total_count：{}'.format(total_count))
    return rentRecords, has_more_data, total_count


def get_history_list(city_id, community_id, offset, min_price, max_price):
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
    if min_price > 0:
        payload["min_price"] = min_price
    if max_price > 0:
        payload["max_price"] = max_price
    logging.info('获取小区成交记录，offset：{}'.format(offset))
    data = get_data(url, payload, method='GET')
    total_count = data["total_count"]
    has_more_data = data["has_more_data"]
    records = {}
    if data.__contains__("list"):
        records = data["list"]
    logging.info('获取小区成交记录，total_count：{}'.format(total_count))
    return records, has_more_data, total_count


def get_ershou_list(city_id, community_id, offset, min_price, max_price):
    """
    获取二手房列表
    """
    url = 'http://app.api.lianjia.com/house/ershoufang/searchv4'
    payload = {
        'city_id': city_id,
        'condition': "c" + community_id,
        'limit_count': '20',
        'limit_offset': str(offset)
    }
    if min_price > 0:
        payload["min_price"] = min_price
    if max_price > 0:
        payload["max_price"] = max_price
    logging.info('获取二手房列表，community_id:{} offset：{}'.format(
        community_id, offset))
    data = get_data(url, payload, method='GET')
    oldhouses = {}
    has_more_data = False
    total_count = 0
    if data.__contains__("list"):
        oldhouses = data["list"]
    if data.__contains__("has_more_data"):
        has_more_data = data["has_more_data"] == 1
    if data.__contains__("total_count"):
        total_count = data["total_count"]

    return oldhouses, has_more_data, total_count



def get_oldhouse_history(db_session, city_id, community_id, min_price, max_price):
    offset = 0
    has_more_data = True
    while has_more_data:
        time.sleep(random.randint(0, config.request_max_gap))
        records, has_more_data, total_count = get_history_list(
            city_id, community_id, offset, min_price, max_price)
        offset = offset + 20
        for aRecord in records:
            record = HistoryRecord(city_id, community_id,
                                   aRecord)
            db_session.merge(record)
        db_session.commit()


def get_oldhouse(db_session, city_id, community_id, min_price, max_price):
    offset = 0
    has_more_data = True
    while has_more_data:
        time.sleep(random.randint(0, config.request_max_gap))
        oldhouses, has_more_data, total_count = get_ershou_list(
            city_id, community_id, offset, min_price, max_price)
        offset = offset + 20
        for aOldhouse in oldhouses:
            oldHouse = OldHouse(city_id, community_id, aOldhouse)
            if oldHouse.house_code and len(oldHouse.house_code) > 0:
                db_session.merge(oldHouse)
        db_session.commit()


def get_rents(db_session, city_id, community_id, price_type):
    offset = 0
    has_more_data = True
    while has_more_data:
        time.sleep(random.randint(0, config.request_max_gap))
        rents, has_more_data, total_count = get_zufang_list(
            city_id, community_id, offset, price_type)
        offset = offset + 20
        for rent in rents:
            rentHouse = RentHouse(city_id, community_id, rent)
            if rentHouse.house_code and len(rentHouse.house_code) > 0:
                db_session.merge(rentHouse)
        db_session.commit()


def get_rent_historys(db_session, city_id, community_id, price_type):
    offset = 0
    has_more_data = True
    while has_more_data:
        time.sleep(random.randint(0, config.request_max_gap))
        rent_historys, has_more_data, total_count = get_zufang_history(
            city_id, community_id, offset, price_type)
        offset = offset + 20
        for rent_history in rent_historys:
            rentRecord = RentRecord(city_id, community_id, rent_history)
            if rentRecord.house_code and len(rentRecord.house_code) > 0:
                db_session.merge(rentRecord)
        db_session.commit()


def main():
    db_session = Session()

    city_id = config.city_id
    district_id = config.district_id
    # 检查是否支持该城市
    allcities = db_session.query(City).all()
    city = db_session.query(City).filter(City.city_id == city_id).first()
    if not allcities or len(allcities) <= 0:
        logging.error('请先更新城市列表！')
        return

    if not city:
        logging.error('不支持该城市 ：{}'.format(city_id))
        return
    allcommunities = db_session.query(Community).filter(Community.city_id == city_id,Community.community_id =='1111027375191').all()
    district = None
    if district_id and district_id != 0:
        alldistricts = db_session.query(District).all()
        district = db_session.query(District).filter(
            City.city_id == city_id, District.district_id == district_id).first()
        if not alldistricts or len(alldistricts) <= 0:
            logging.error('请先获取该城市的基本信息！')
            return
    
        if not district:
            logging.error('该城市没有 {} 该行政区 ：{}'.format(city_id, district_id))
            return
    
        allcommunities = db_session.query(
        Community).filter(Community.city_id == city_id, Community.district_name == district.district_name).all()
    
    total_communities = len(allcommunities)

    show_district_id = 0
    show_district_name = ""
    if district:
        show_district_id = district_id
        show_district_name = district.district_name
    logging.info('开始按小区抓取， 城市：{} ,行政区：{}({})， 共有小区 ：{}'.format(
        city_id, show_district_id,show_district_name , len(allcommunities)))
    index = 1
    for aCommunity in allcommunities:
        # 处理小区详细信息
        community_id = aCommunity.community_id
        logging.info(
            '开始获取该小区详细信息：{}  , {}/{}'.format(community_id, index, total_communities))
        index = index + 1
        data = get_xiaoqu_info(community_id)
        community_info = CommunityInfo(city_id, data)
        db_session.merge(community_info)
        db_session.commit()

        _, _, oldhouseNum = get_ershou_list(city_id, community_id, 0, 0, 0)
        _, _, recordNum = get_history_list( city_id, community_id, 0, 0, 0)
        _, _, rentNum = get_zufang_list(city_id, community_id, 0, 0)
        _, _, rentRecordNum = get_zufang_history(city_id, community_id, 0, 0)

        # 获取小区二手房信息
        logging.info('开始获取该小区二手房信息：{}'.format(community_id))
        price_list = [{"min": 0, "max": 100},
                      {"min": 100, "max": 150},
                      {"min": 150, "max": 200},
                      {"min": 200, "max": 250},
                      {"min": 250, "max": 300},
                      {"min": 300, "max": 500},
                      {"min": 500, "max": 1000},
                      {"min": 1000, "max": 0}]
        # 如果记录数大于2000 ，会出现重复数据，会根据价格再次筛选
        if oldhouseNum >= 2000:
            for priceItem in price_list:
                get_oldhouse(db_session, city_id, community_id,
                             priceItem["min"], priceItem["max"])
        else:
            get_oldhouse(db_session, city_id, community_id, 0, 0)
        logging.info('完成获取该小区二手房信息：{}'.format(community_id))
        # 获取小区成交信息
        logging.info('开始获取该小区历史成交信息：{}'.format(community_id))
        price_list = [{"min": 0, "max": 100},
                      {"min": 100, "max": 150},
                      {"min": 150, "max": 200},
                      {"min": 200, "max": 250},
                      {"min": 250, "max": 300},
                      {"min": 300, "max": 500},
                      {"min": 500, "max": 1000},
                      {"min": 1000, "max": 0}]
        # 如果记录数大于2000 ，会出现重复数据，会根据价格再次筛选
        if recordNum >= 2000:
            for priceItem in price_list:
                get_oldhouse_history(db_session, city_id, community_id,
                            priceItem["min"], priceItem["max"])
        else:
            get_oldhouse_history(db_session, city_id, community_id, 0, 0)
        logging.info('完成获取该小区历史成交信息：{}'.format(community_id))
        # 获取小区成交信息
        logging.info('开始获取该小区租房信息：{}'.format(community_id))
        # 如果记录数大于2000 ，会出现重复数据，会根据价格再次筛选
        if recordNum >= 2000:
            for priceItem in xrange(1, 11):
                get_rents(db_session, city_id, community_id, priceItem)
        else:
            get_rents(db_session, city_id, community_id, 0)
        logging.info('完成获取该小区租房信息：{}'.format(community_id))
        # 获取小区租房记录
        logging.info('开始获取该小区租房记录信息：{}'.format(community_id))
        # 如果记录数大于2000 ，会出现重复数据，会根据价格再次筛选
        if recordNum >= 2000:
            for priceItem in xrange(1, 11):
                get_rent_historys(db_session, city_id, community_id, priceItem)
        else:
            get_rent_historys(db_session, city_id, community_id, 0)
        logging.info('完成获取该小区租房记录信息：{}'.format(community_id))
    logging.info('完成小区信息抓取， 城市：{} ,行政区：{}({})'.format(
        city_id, show_district_id, show_district_name))
    db_session.commit()
    db_session.close()

if __name__ == '__main__':
    main()
