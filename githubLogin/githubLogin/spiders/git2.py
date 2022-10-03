import scrapy


class Git2Spider(scrapy.Spider):
    name = 'git2'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        # 从登录页面响应中解析出 post数据
        token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        timestamp = response.xpath("//input[@name='timestamp']/@value").extract_first()
        timestamp_secret = response.xpath("//input[@name='timestamp_secret']/@value").extract_first()

        post_data = {
            "commit": "Sign in",
            "authenticity_token": token,
            "login": "1164814322@qq.com",
            "password": "15917845180zjj",
            "webauthn-support": "supported",
            "webauthn-iuvpaa-support": "unsupported",
            "return_to": "https://github.com/login",
            # "allow_signup":
            # "client_id":
            # "integration":
            # "required_field_4d96":
            "timestamp": timestamp,
            "timestamp_secret": timestamp_secret
        }

        # print("111", post_data)
        # 针对登录url发送post请求
        yield scrapy.FormRequest(
            url = "https://github.com/session",
            formdata=post_data,
            callback=self.after_login
        )

    def after_login(self, response):
        yield scrapy.Request(url="https://github.com/kaskeh",
                             callback=self.check_login)

    def check_login(self, response):
        print(response.xpath("/html/head/title/text()").extract_first())