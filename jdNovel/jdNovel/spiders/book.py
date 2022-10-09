import scrapy
import json

from jdNovel.items import JdnovelItem

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com']
    # # 修改起始的url
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # # 获取所有图书大分类节点列表
        # big_node_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        # print("big_node_list", len(big_node_list))
        url = 'https://pjapi.jd.com/book/sort?source=bookSort&callback=jsonp_1665152330065_37596'
        yield scrapy.Request(url, callback=self.paser_big_category)

    def paser_big_category(self, response):
        json_data = json.loads(response.body.decode("utf-8")[26:-1])
        # print("json_data", json_data)

        big_category_model = 'https://channel.jd.com/{fatherCategoryId}-{categoryId}.html'
        small_category_model = 'https://list.jd.com/list.html?cat={fatherCategoryId},{categoryId},{sonCategoryId}'

        for big_category in json_data["data"][:1]:
            # print("big_category", big_category)
            fatherCategoryId = int(big_category["fatherCategoryId"])
            categoryId = int(big_category["categoryId"])
            categoryName = big_category["categoryName"]
            # 拼接大分类
            big_category_url = big_category_model.format(fatherCategoryId=fatherCategoryId,
                                                         categoryId=categoryId)
            for small_category in big_category["sonList"]:
                sonCategoryId = int(small_category["categoryId"])
                sonCategoryName = small_category["categoryName"]
                # 拼接小分类
                small_cateagory_url = small_category_model.format(fatherCategoryId=fatherCategoryId,
                                                                  categoryId=categoryId,
                                                                  sonCategoryId=sonCategoryId)
                # print("big_category_url", big_category_url, "small_cateagory_url", small_cateagory_url)
                # 现查看直接提出出来的数据是带小数点的，与正确链接不太相符，故进行int()处理
                # big_category_url https://channel.jd.com/1713.0-25558.0.html small_cateagory_url https://list.jd.com/list.html?cat=1713.0,25558.0,25559.0

                # 保存父分类信息，让图书有相应的分类信息
                temp = {}
                temp["big_categoryName"] = categoryName
                temp["big_category_url"] = big_category_url
                temp["small_categoryName"] = sonCategoryName
                temp["small_cateagory_url"] = small_cateagory_url

                # 模拟点击小分类链接
                yield scrapy.Request(url=small_cateagory_url,
                                     meta={"py21": temp},
                                     callback=self.parse_book_list,
                                     # dont_filter=True
                                     )

    def parse_book_list(self, response):
        temp = response.meta["py21"]
        book_list = response.xpath("//*[@id='J_goodsList']/ul/li/div")
        print("spider 收到了中间件传来的数据", len(book_list))

        for book in book_list:

            item = JdnovelItem()

            item["big_category"] = temp["big_categoryName"]
            item["big_category_link"] = temp["big_category_url"]
            item["small_category"] = temp["small_categoryName"]
            item["small_category_link"] = temp["small_cateagory_url"]

            item["author"] = book.xpath("./div[4]/span[1]/span/a/text()").extract_first()
            item["bookName"] = book.xpath("./div[3]/a/em/text()").extract_first()
            item["link"] = book.xpath("./div[1]/a/@href()").extract_first()
            item["price"] = book.xpath("./div[3]/a/em/text()").extract_first()
            item["skuid"] = book.xpath("./div[3]/a/em/text()").extract_first()

            yield item


