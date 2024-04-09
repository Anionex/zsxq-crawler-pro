**如果觉得本项目有用，欢迎fork&star!**

## 模拟登陆
爬取的是网页版知识星球，https://wx.zsxq.com/dweb/#。

这个网站并不是依靠 cookie 来判断你是否登录，而是请求头中的 Authorization 字段。

所以，需要把 Authorization，User-Agent 换成你自己的。（注意 User-Agent 也要换成你自己的）

代码中找到如下字段更改，Authorization，User-Agent可在网络活动检测处获取（edge为F12

 ```python
headers = {
    'Authorization': '3704A4EE-377E-1C88-B031-0A42D9E9Bxxx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}
 ```

## 使用说明：
链接入口获取，浏览器开发选项网络检测异步加载/XHR，找到topics?字样链接，比如https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&count=20，即为入口
程序中还需填入
urls.txt写入链接，一个一行。
titles.txt写入标签名称，一个一行，和urls顺序对应。

爬虫将会逐个爬取urls中的链接，生成pdf。

技术交流，欢迎链接wx：anion1314
