import requests
import re
from lxml import etree

def get_alert():
    s = requests.session()
    data={'txtUserName':'gsyuan','txtPassword':'******'}
    s.post('http://home:8000/Logon.aspx?action=logout',data)
    url='http://home:8000/WindEIP/RDMS/FunctionModule/ExperienceDisplay.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    content=requests.get(url,headers=headers,data=data)
    html=etree.HTML(content.content)
    print(content.cookies)

    product_xpath='//*[@id="txtMyProduct"]'
    module_xpath='//*[@id="txtMyModuleName"]'
    para_xpath='//*[@id="hasTask"]/table/tbody/tr[1]/td[5]/label/text()'
    rule_xpath='//*[@id="txtMyRuleName"]'

    product=html.xpath(product_xpath)
    module=html.xpath(module_xpath)
    para=html.xpath(para_xpath)
    rule=html.xpath(rule_xpath)
    print(product,module,para,rule)
    print(content)


m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
p = re.compile(r'(\w+) (\w+)(?P<sign>.*)', re.DOTALL)
print(m.expand(r'test \2 \1\3'))