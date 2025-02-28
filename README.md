# Clash 订阅规则过滤器

在使用AI网站或Web3时，订阅的规则里包含一些香港节点，使用自动模式时，经常会切到香港节点，导致访问这些网站异常.
因此用AI写了一个简单的转换脚本，去掉香港(也可以自定义其它的过滤关键字)节点。

# Usage

1. 安装依赖: `pip install -r requirements.txt`
2. 如果要指定排除其它节点（不需要则跳过），则修改脚本 filter.py 第22行中的HongKong和HK：`if 'HongKong' in name or 'HK' in name:` 
3. 生成新的规则文件：`/usr/bin/python3 filter.py 订阅url rules.yaml` 
4. 启动一个简单Web服务器：`nohup python -m http.server 8000 &`
5. 在 Clash 订阅新的 URL:  http://127.0.0.1:8000/rules.yaml

Tips:
* 第3步可以写一个定时任务，定时更新。
* 第4步只是把文件放到一个Web服务器中，如果放nginx，可以用下面的配置(在conf.d中创建clashx.conf配置文件)：
```nginx
server {
    listen         8000;
    listen         [::]:8000;
    server_name    clashx;
    root           /var/www/clashx;
    autoindex on;  //自动显示目录
}
```

