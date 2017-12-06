# encoding: utf-8
import logging
from .orm import Base
from sqlalchemy import Column, types, PrimaryKeyConstraint
import json

# 城市【城市id、城市名称】


class City(Base):
    __tablename__ = 'cities'

    city_id = Column(types.Integer, primary_key=True)
    city_name = Column(types.String(128), nullable=False)
    abbr = Column(types.String(128), nullable=False)
    m_url = Column(types.String(1024), nullable=False)

    def __init__(self, info):
        self.city_id = info['city_id']
        self.city_name = info['city_name']
        self.abbr = info['abbr']
        self.m_url = ''
        if info.__contains__("m_url"):
            self.m_url = info['m_url']

# 行政区域


class District(Base):
    __tablename__ = 'districts'
    __table_args__ = (
        PrimaryKeyConstraint('city_id', 'district_id'),
    )
    city_id = Column(types.Integer)
    district_id = Column(types.Integer)
    district_name = Column(types.String(128), nullable=False)
    quanpin = Column(types.String(32), nullable=False)
    # latitude = Column(types.String(32), nullable=False)
    # longitude = Column(types.String(32), nullable=False)

    def __init__(self, city_id, info):
        self.city_id = city_id
        self.district_id = info['district_id']
        self.district_name = info['district_name']
        self.quanpin = info['district_quanpin']
        # self.latitude = info['latitude']
        # self.longitude = info['longitude']

# 地铁线


class Subway(Base):
    __tablename__ = 'subways'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'subway_line_id'),)
    city_id = Column(types.Integer)
    subway_line_id = Column(types.String(128), nullable=False)
    subway_line_name = Column(types.String(128), nullable=False)
    baidu_subway_line_id = Column(types.String(64), nullable=False)
    latitude = Column(types.String(32), nullable=False)
    longitude = Column(types.String(32), nullable=False)

    def __init__(self, city_id, info):
        self.city_id = city_id
        self.subway_line_id = info['subway_line_id']
        self.subway_line_name = info['subway_line_name']
        self.baidu_subway_line_id = info['baidu_subway_line_id']
        self.latitude = info['latitude']
        self.longitude = info['longitude']

# 小区


class Community(Base):
    __tablename__ = 'communities'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'community_id'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)
    community_name = Column(types.String(128), nullable=False)
    district_name = Column(types.String(128), nullable=False)
    bizcircle_name = Column(types.String(128), nullable=False)
    building_finish_year = Column(types.String(32), nullable=False)
    building_type = Column(types.String(32), nullable=False)
    avg_unit_price = Column(types.String(32), nullable=False)
    ershoufang_source_count = Column(types.String(32), nullable=False)
    ershoufang_avg_unit_price = Column(types.String(32), nullable=False)
    neo_desc = Column(types.String(2048), nullable=False)

    def __init__(self, city_id, info):
        self.city_id = city_id
        self.community_id = ''
        if info.__contains__("community_id"):
            self.community_id = info['community_id']
        self.community_name = ''
        if info.__contains__("community_name"):
            self.community_name = info['community_name']
        self.district_name = ''
        if info.__contains__("district_name"):
            self.district_name = info['district_name']
        self.bizcircle_name = ''
        if info.__contains__("bizcircle_name"):
            self.bizcircle_name = info['bizcircle_name']
        self.building_finish_year = ''
        if info.__contains__("building_finish_year"):
            self.building_finish_year = info['building_finish_year']
        self.building_type = ''
        if info.__contains__("building_type"):
            self.building_type = info['building_type']
        self.avg_unit_price = ''
        if info.__contains__("avg_unit_price"):
            self.avg_unit_price = info['avg_unit_price']
        self.ershoufang_source_count = ''
        if info.__contains__("ershoufang_source_count"):
            self.ershoufang_source_count = info['ershoufang_source_count']
        self.ershoufang_avg_unit_price = ''
        if info.__contains__("ershoufang_avg_unit_price"):
            self.ershoufang_avg_unit_price = info['ershoufang_avg_unit_price']
        self.neo_desc = ''
        if info.__contains__("neo_desc"):
            self.neo_desc = info['neo_desc']

# 小区详情


class CommunityInfo(Base):
    __tablename__ = 'community_info'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'community_id'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)  # 小区编号
    community_name = Column(types.String(128), nullable=False)  # 小区名
    district_name = Column(types.String(32), nullable=False)  # 行政区名称
    bizcircle_name = Column(types.String(128), nullable=False)  # 商圈名称
    ershoufang_source_count = Column(
        types.String(32), nullable=False)  # 在售二手房数量
    address = Column(types.String(256), nullable=False)  # 小区地址
    favorite_count = Column(types.String(32), nullable=False)  # 关注人数
    location = Column(types.String(1024), nullable=False)  # 位置描述
    point_lat = Column(types.String(32), nullable=False)  # 经度
    point_lng = Column(types.String(32), nullable=False)  # 纬度
    price = Column(types.String(32), nullable=False)  # 10月份参考均价
    history_record = Column(types.String(32), nullable=False)  # 历史成交数量
    rent_number = Column(types.String(32), nullable=False)  # 在租房源数量
    brief_list = Column(types.Text, nullable=False)  # 附加属性 建筑年代 统计用途 开发商
    quality = Column(types.Text, nullable=False)  # 小区品质
    surroundings = Column(types.Text, nullable=False)  # 周边配套
    buildings = Column(types.Text, nullable=False)  # 楼栋户型

    def __init__(self, city_id, info):
        self.city_id = city_id
        # basic info
        self.community_id = ''
        self.community_name = ''
        self.district_name = ''
        self.bizcircle_name = ''
        self.ershoufang_source_count = ''
        self.address = ''
        self.favorite_count = ''
        self.location = ''
        self.point_lat = ''
        self.point_lng = ''
        self.price = ''
        self.history_record = ''
        self.rent_number = ''
        self.brief_list = ''
        if info.__contains__("basic_info"):
            basic_info = info['basic_info']
            self.community_id = basic_info['id']
            if basic_info.__contains__("name"):
                self.community_name = basic_info["name"]
            if basic_info.__contains__("district_name"):
                self.district_name = basic_info["district_name"]
            if basic_info.__contains__("bizcircle_name"):
                self.bizcircle_name = basic_info["bizcircle_name"]
            if basic_info.__contains__("ershoufang_source_count"):
                self.ershoufang_source_count = basic_info[
                    "ershoufang_source_count"]
            if basic_info.__contains__("address"):
                self.address = basic_info["address"]
            if basic_info.__contains__("favorite_count"):
                self.favorite_count = basic_info["favorite_count"]
            if basic_info.__contains__("location"):
                self.location = basic_info["location"]
            if basic_info.__contains__("point_lat"):
                self.point_lat = basic_info["point_lat"]
            if basic_info.__contains__("point_lng"):
                self.point_lng = basic_info["point_lng"]
            if basic_info.__contains__("price"):
                price_info = basic_info["price"]
                if price_info.__contains__("desc"):
                    self.price = price_info["desc"]
            if basic_info.__contains__("sold"):
                sold_info = basic_info["sold"]
                if sold_info.__contains__("desc"):
                    self.history_record = sold_info["desc"]
            if basic_info.__contains__("rent"):
                rent_info = basic_info["sold"]
                if rent_info.__contains__("desc"):
                    self.rent_number = rent_info["desc"]
            if basic_info.__contains__("brief_list"):
                self.brief_list = str(basic_info["brief_list"])
        # 小区品质
        self.quality = ''
        if info.__contains__("quality"):
            self.quality = str(info["quality"])
        # 周边配套
        self.surroundings = ''
        if info.__contains__("surroundings"):
            self.surroundings = str(info["surroundings"])

        self.buildings = ''
        if info.__contains__("buildings"):
            self.buildings = str(info["buildings"])

# 二手房


class OldHouse(Base):
    __tablename__ = 'old_houses'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'house_code'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)
    house_code = Column(types.String(128), nullable=False)
    title = Column(types.String(1024), nullable=False)
    desc = Column(types.String(1024), nullable=False)
    community_name = Column(types.String(128), nullable=False)
    blueprint_hall_num = Column(types.String(32), nullable=False)
    blueprint_bedroom_num = Column(types.String(32), nullable=False)
    area = Column(types.String(32), nullable=False)
    price = Column(types.String(32), nullable=False)
    unit_price = Column(types.String(32), nullable=False)
    card_type = Column(types.String(32), nullable=False)
    is_foucs = Column(types.String(32), nullable=False)
    tags = Column(types.Text, nullable=False)
    info_list = Column(types.Text, nullable=False)

    def __init__(self, city_id,community_id, info):
        self.city_id = city_id
        self.community_id = community_id
        self.house_code = ''
        if info.__contains__("house_code"):
            self.house_code = info['house_code']
        self.community_name = ''
        if info.__contains__("community_name"):
            self.community_name = info['community_name']
        self.title = ''
        if info.__contains__("title"):
            self.title = info['title']
        self.desc = ''
        if info.__contains__("desc"):
            self.desc = info['desc']
        self.blueprint_hall_num = ''
        if info.__contains__("blueprint_hall_num"):
            self.blueprint_hall_num = info['blueprint_hall_num']
        self.blueprint_bedroom_num = ''
        if info.__contains__("blueprint_bedroom_num"):
            self.blueprint_bedroom_num = info['blueprint_bedroom_num']
        self.area = ''
        if info.__contains__("area"):
            self.area = info['area']
        self.price = ''
        if info.__contains__("price"):
            self.price = info['price']
        self.unit_price = ''
        if info.__contains__("unit_price"):
            self.unit_price = info['unit_price']
        self.card_type = ''
        self.card_type = ''
        if info.__contains__("card_type"):
            self.card_type = info['card_type']
        self.is_foucs = ''
        if info.__contains__("is_foucs"):
            self.is_foucs = info['is_foucs']
        self.tags = ''
        if info.__contains__("color_tags"):
            color_tags = info["color_tags"]
            temp = ''
            for tag in color_tags:
                temp = temp + "," + tag["desc"]
            self.tags = temp

        self.info_list = ''
        if info.__contains__("info_list"):
            self.info_list = str(info["info_list"])


# 成交记录
class HistoryRecord(Base):
    __tablename__ = 'hisoty_records'
    __table_args__ = (PrimaryKeyConstraint(
        'city_id', 'house_code', 'sign_timestamp'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)
    bizcircle_id = Column(types.String(128), nullable=False)
    house_code = Column(types.String(128), nullable=False)
    title = Column(types.String(1024), nullable=False)
    new_title = Column(types.String(1024), nullable=False)
    kv_house_type = Column(types.String(32), nullable=False)
    frame_id = Column(types.String(32), nullable=False)
    blueprint_hall_num = Column(types.String(32), nullable=False)
    blueprint_bedroom_num = Column(types.String(32), nullable=False)
    area = Column(types.String(32), nullable=False)
    price = Column(types.String(32), nullable=False)
    unit_price = Column(types.String(128), nullable=False)
    sign_date = Column(types.String(256), nullable=False)
    sign_timestamp = Column(types.String(128), nullable=False)
    sign_source = Column(types.String(128), nullable=False)
    orientation = Column(types.String(128), nullable=False)
    floor_state = Column(types.String(128), nullable=False)
    building_finish_year = Column(types.String(128), nullable=False)
    decoration = Column(types.String(128), nullable=False)
    building_type = Column(types.String(128), nullable=False)

    def __init__(self, city_id,community_id, info):
        self.city_id = city_id
        self.community_id = community_id
        self.bizcircle_id = ''
        if info.__contains__("bizcircle_id"):
            self.bizcircle_id = info['bizcircle_id']
        self.house_code = ''
        if info.__contains__("house_code"):
            self.house_code = info['house_code']
        self.title = ''
        if info.__contains__("title"):
            self.title = info['title']
        self.new_title = ''
        if info.__contains__("new_title"):
            self.new_title = info['new_title']
        self.kv_house_type = ''
        if info.__contains__("kv_house_type"):
            self.kv_house_type = info['kv_house_type']
        self.frame_id = ''
        if info.__contains__("frame_id"):
            self.frame_id = info['frame_id']
        self.blueprint_hall_num = ''
        if info.__contains__("blueprint_hall_num"):
            self.blueprint_hall_num = info['blueprint_hall_num']
        self.blueprint_bedroom_num = ''
        if info.__contains__("blueprint_bedroom_num"):
            self.blueprint_bedroom_num = info['blueprint_bedroom_num']
        self.area = ''
        if info.__contains__("area"):
            self.area = info['area']
        self.price = ''
        if info.__contains__("price"):
            self.price = info['price']
        self.unit_price = ''
        if info.__contains__("unit_price"):
            self.unit_price = info['unit_price']
        self.sign_date = ''
        if info.__contains__("sign_date"):
            self.sign_date = info['sign_date']
        self.sign_timestamp = ''
        if info.__contains__("sign_timestamp"):
            self.sign_timestamp = info['sign_timestamp']
        self.sign_source = ''
        if info.__contains__("sign_source"):
            self.sign_source = info['sign_source']
        self.orientation = ''
        if info.__contains__("orientation"):
            self.orientation = info['orientation']
        self.floor_state = ''
        if info.__contains__("floor_state"):
            self.floor_state = info['floor_state']
        self.building_finish_year = ''
        if info.__contains__("building_finish_year"):
            self.building_finish_year = info['building_finish_year']
        self.decoration = ''
        if info.__contains__("decoration"):
            self.decoration = info['decoration']
        self.building_type = ''
        if info.__contains__("building_type"):
            self.building_type = info['building_type']

# 出租房


class RentHouse(Base):
    __tablename__ = 'rent_houses'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'house_code'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)
    house_code = Column(types.String(128), nullable=False)
    kv_house_type = Column(types.String(32), nullable=False)
    title = Column(types.String(128), nullable=False)
    area = Column(types.String(32), nullable=False)
    price = Column(types.String(32), nullable=False)
    desc = Column(types.String(2048), nullable=False)
    is_ziroom = Column(types.String(32), nullable=False)
    is_foucs = Column(types.String(32), nullable=False)
    tags = Column(types.String(2048), nullable=False)

    def __init__(self, city_id,community_id, info):
        self.city_id = city_id
        self.community_id = community_id
        self.house_code = ''
        if info.__contains__("house_code"):
            self.house_code = info['house_code']
        self.title = ''
        if info.__contains__("title"):
            self.title = info['title']
        self.kv_house_type = ''
        if info.__contains__("kv_house_type"):
            self.kv_house_type = info['kv_house_type']
        self.area = ''
        if info.__contains__("area"):
            self.area = info['area']
        self.price = ''
        if info.__contains__("price"):
            self.price = info['price']
        self.desc = ''
        if info.__contains__("desc"):
            self.desc = info['desc']
        self.is_ziroom = ''
        if info.__contains__("is_ziroom"):
            self.is_ziroom = info['is_ziroom']
        self.is_foucs = ''
        if info.__contains__("is_foucs"):
            self.is_foucs = info['is_foucs']
        self.tags = ''
        if info.__contains__("color_tags"):
            color_tags = info["color_tags"]
            temp = ''
            for tag in color_tags:
                temp = temp + "," + tag["desc"]
            self.tags = temp

# 出租记录


class RentRecord(Base):
    __tablename__ = 'rent_records'
    __table_args__ = (PrimaryKeyConstraint('city_id', 'house_code'),)
    city_id = Column(types.Integer)
    community_id = Column(types.String(128), nullable=False)
    house_code = Column(types.String(128), nullable=False)
    kv_house_type = Column(types.String(32), nullable=False)
    title = Column(types.String(128), nullable=False)
    price_str = Column(types.String(32), nullable=False)
    price_unit = Column(types.String(32), nullable=False)
    desc = Column(types.String(2048), nullable=False)
    is_ziroom = Column(types.String(32), nullable=False)
    sign_time = Column(types.String(32), nullable=False)

    def __init__(self, city_id,community_id, info):
        self.city_id = city_id
        self.community_id = community_id
        self.house_code = ''
        if info.__contains__("house_code"):
            self.house_code = info['house_code']
        self.title = ''
        if info.__contains__("title"):
            self.title = info['title']
        self.kv_house_type = ''
        if info.__contains__("kv_house_type"):
            self.kv_house_type = info['kv_house_type']
        self.price_unit = ''
        if info.__contains__("price_unit"):
            self.price_unit = info['price_unit']
        self.price_str = ''
        if info.__contains__("price_str"):
            self.price_str = info['price_str']
        self.desc = ''
        if info.__contains__("desc"):
            self.desc = info['desc']
        self.is_ziroom = ''
        if info.__contains__("is_ziroom"):
            self.is_ziroom = info['is_ziroom']
        self.sign_time = ''
        if info.__contains__("sign_time"):
            self.sign_time = info['sign_time']

