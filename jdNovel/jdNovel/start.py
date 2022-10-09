from scrapy import cmdline

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute("scrapy crawl book --nolog".split())
# begin = time.time()
# while True:
#     if begin + 10 < time.time():
#         print(time.time())
#         break