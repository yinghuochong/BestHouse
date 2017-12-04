# Get BestHouse
Get info from lianjia app

### 准备工作：

1、安装 **python3.6** 以上版本

2、安装MySql

3、下载代码,并进入BestHouse目录

`git clone https://github.com/yinghuochong/BestHouse.git`

4、安装依赖的python库, **如果有问题加 sudo**

`pip3 install -r requirements.txt`

### 使用方法：

1、修改配置：
在conf目录下新建 config.json，配置数据库信息

2、获取所有城市列表：

`python3 get_cities.py`

会写到数据库里的cities表

3、根据城市编号获取指定城市的相关信息，包括行政区、地铁。比如获取北京城市信息

`python3 get_city_info.py 110000`

结果会写到 districts 和 subways 表

4、根据城市编号获取指定城市所有 小区列表

`python3 get_xiaoqu_list.py 110000`

结果会写到 communities 表

5、根据城市编号获取指定城市所有小区的详细信息，包括小区详情、小区在售二手房、小区成交历史、小区在租房源

`python3 get_xiaoqu_info.py 110000`

结果会写到 community_info 、hisoty_records、rent_houses、old_houses 表




### 备注
Thanks [CaoZ](https://github.com/CaoZ/Fast-LianJia-Crawler)

ref:[https://github.com/CaoZ/Fast-LianJia-Crawler](https://github.com/CaoZ/Fast-LianJia-Crawler)