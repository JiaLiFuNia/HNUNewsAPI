## [HNU](https://www.htu.edu.cn/)新闻api
该项目使用GitHub+Vercel搭建，使用Python+flask框架实现，获取的数据来源于[河南师范大学官网](https://www.htu.edu.cn/)，本项目已开源在[GitHub](https://github.com/JiaLiFuNia/HNUNewsAPI)  

__请求地址：http://hnu.xhand.fun/__  
### __GET请求：__  
|  类型   |           请求链接           |
|:-----:|:------------------------:|
| 通知公告  | http://hnu.xhand.fun/an  |
| 院部动态  | http://hnu.xhand.fun/bn  |
| 学术预告  | http://hnu.xhand.fun/cn  |
| 师大新闻  | http://hnu.xhand.fun/dn  |
| 主页轮播图 | http://hnu.xhand.fun/pic |


### __POST请求：__  
#### 请求参数
|  字段   | 说明 |   类型   |        备注        | 是否必填 |
|:-----:|:--:|:------:|:----------------:|:----:|
| types | 类型 | String |        无         |  是   |
| count | 数量 |  Int   | 0 < count <= 100 |  是   |

#### types
| 值  |  说明  |      | 值  |  说明  |
|:--:|:----:|:----:|:--:|:----:|
| an | 通知公告 |      | aj | 教学新闻 |
| bn | 新闻速递 |      | bj | 教务通知 |
| cn | 学术预告 |      | cj | 公示公告 |
| dn | 师大新闻 |      | dj | 考务管理 |

### __返回参数：__
|   字段    |  说明   |   类型   |
|:-------:|:-----:|:------:|
|  code   | 接口状态码 |  Int   |
| message | 接口信息  | String |
|  data   |  数据   | Object |

#### data
|   值   |  说明  |
|:-----:|:----:|
|  id   |  ID  |
| time  |  时间  |
| title |  标题  |
|  url  | 详细链接 |
