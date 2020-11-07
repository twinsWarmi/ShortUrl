## 環境配置
> 請在 .env檔案裡配置

### 服務位置
配置 APP_HOST(host), APP_PORT(port)

default: 127.0.0.1:5000

### redis
配置 REDIS_HOST(host), REDIS_PORT(port), REDIS_DB(db)

default: 127.0.0.1:6379/0
### 短網址路徑長度
> 支援短網址數量為 62的 PATH_LENGTH次方  
> ex. PATH_LENGTH=2, 可支援 62*62=3844個短網址

配置 PATH_LENGTH(length)

default: 5


## API


### 使用者介面
提供簡單的使用者介面
``` shell= 
{host}:{port}
```

### 取得短網址
將原始 url轉為短網址
``` shell= 
{host}:{port}/short_url
```

**Input Data**

| Field    | Type   | Required or not | Description       |
| -------- | ------ | --------------- | ----------------- |
|   url    | String | Required        | 欲轉換短網址的網址   |

**Sample Input**

```
GET:
http://127.0.0.1:5000/short_url?url=https://teaches.cc/
POST:
body: {"url": "https://teaches.cc/"}
```
**Output Data**

| Field       | Type         | Description          |
| ----------- | ------------ | -------------------- |
| code        | Int          | status code          |
| status      | String       | status description   |
| message     | String       | information          |

**Sample Output**

```
{"code": 200, "status": "success", "msg": "http://127.0.0.1:5000/WKxXN"}
```

### 取得原始網址
從短網址取得原始 url路徑
``` shell= 
{host}:{port}/{url}
```

**Sample Input**

```
GET/POST:
http://127.0.0.1:5000/WKxXN
```

**Output Data**

| Field       | Type         | Description          |
| ----------- | ------------ | -------------------- |
| code        | Int          | status code          |
| status      | String       | status description   |
| message     | String       | information          |

**Sample Output**

```
//success
{"code": 200, "status": "success", "msg": "https://teaches.cc/"}
//error
{"code": 400, "status": "error", "msg": "No such url!"}
```


## 運行 

### 運行指令
``` shell=
$ python main.py
```
   
終端機顯示 Running on ...，進入網址後即可看到： 
``` shell=
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
   
### 警吿
若顯示警告：
``` 
WARNING: This is a development server. Do not use it in a production deployment.
```

代表目前使用的環境是 production，若不想看到這行警告，需將 FLASK_ENV環境設置成
development的模式
``` shell=
    $ export FLASK_ENV=development
```


## 測試

### unittest
先到項目路徑下
``` shell=
$ python -m unittest -v
```

### coverage

須先安裝 coverage
```
$ pip install coverage 
```

先到項目路徑下
```
$ coverage run tests/test_main.py -v
```


