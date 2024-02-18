## [HNU](https://www.htu.edu.cn/)新闻api
该项目是由使用GitHub+Vercel搭建，使用Python实现，所返回的数据是在[HNU](https://www.htu.edu.cn/)官网上进行爬取，本项目已开源在[GitHub](https://github.com/JiaLiFuNia/HNUNewsAPI/tree/master)  


__请求地址：http://hnu.xhand.fun/__  
__GET请求参数：__  
类型     | 请求链接
:-----: | :-----:
通知公告  | http://hnu.xhand.fun/an
院部动态  | http://hnu.xhand.fun/bn
学术预告  | http://hnu.xhand.fun/cn
师大新闻  | http://hnu.xhand.fun/dn
所有  | http://hnu.xhand.fun<br>http://hnu.xhand.fun/all

__POST请求参数：__  
字段    | 说明     | 类型    |备注              | 是否必填
:-----: | :-----: | :-----: | :-----:          | :-----:
types   | 类型    | String  | 无                | 是
count   | 数量    | Int     | 0 < count <= 100 | 是

types
值      | 说明
:-----: | :-----:
an      | 通知公告
bn      | 院部动态
cn      | 学术预告
dn      | 师大新闻
en      | 媒体师大
all     | 所有

__返回参数：__
字段    | 说明     | 类型   
:-----: | :-----: | :-----:
code   | 接口状态码    | Int
message | 接口信息    | String
data | 数据  | Object

data
值      | 说明
:-----: | :-----:
id      | ID
time    | 时间
title   | 标题
url     | 详细链接
