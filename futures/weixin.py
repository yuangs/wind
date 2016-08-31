
import downloader


def weixin():
    weixin_url="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA4NDg3MDEyNw==&uin=Mzc2NDQxNjgw&key=cf237d7ae24775e875012df81a1d85f398c8b82d22dcce2566b94c7eed5fa702ce897fb2533b33d0183c5a012b0b4de69fda6646b31cb3ee&devicetype=android-23&version=26031932&lang=zh_CN&nettype=ctnet&pass_ticket=u2SNofNIhhIn5ecF5KAsG1rq%2F8U2I62vX3h%2FZB94bWWUvl0CE6uyD81sEtcthctb&wx_header=1#wechat_webview_type=1"
    r = requests.get(weixin_url, headers=headers)
    selector = etree.HTML(weixin_url)
    articles_xpath='//h4[@class="msg_title"]/@hrefs'
    articles =selector.xpath(articles_xpath)
    for i in range(len(articles)):
        downloader.download(articles[i])
        time.sleep(2)