import logging, aiomysql
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web


logging.basicConfig(level=logging.INFO)

# 1 创建web整体框架：
	# 通过异步IO，处理http请求，整个webapp监听着端口的请求
	# 每次服务器端接收到一个请求就建立一个子进程去响应这个请求
	# 提取本地的html文件放入返回的http请求中的body中

# 1.1 index函数负责响应http请求并返回一个html
async def index(request):
	# 返回服务器响应内容
	return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')

# 1.2 将一个生成器扔给eventloop去执行
	# eventloop监听本机ip的9000端口不断接受请求进行处理
async def init(loop):
	# 创建HTTP服务
	app = web.Application(loop=loop)
	# add_route方法设定url为http://127.0.0.1:9000
	# 将index返回的html显示在这个url上
	app.router.add_route('GET', '/', index)
	# 创建TCP连接服务
	srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
	# 将信息记录到日志文件
	logging.info('server started at http://127.0.0.1:9000...')
	return srv


# 创建eventloop对象
loop = asyncio.get_event_loop()
# eventloop接受请求，执行协程init()，直到协程都执行完，程序退出
loop.run_until_complete(init(loop))
# run_forever()是程序不会自动退出
loop.run_forever()