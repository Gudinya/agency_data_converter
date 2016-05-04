"""<?xml version="1.0" encoding="UTF-8"?>
<realty-feed xmlns="http://webmaster.yandex.ru/schemas/feed/realty/2010-06">
    <generation-date>2010-12-11T12:00:00+04:00</generation-date>
  <!-- Минимальный набор полей -->
    <!-- Квартира на вторичном рынке -->
    <offer internal-id="1245">
        <type>продажа</type>
        <property-type>жилая</property-type>
        <category>квартира</category>

        <url>http://yandex.ru/1/</url>
        <creation-date>2010-11-13T12:32:45+04:00</creation-date>

        <location>
            <country>Россия</country>
            <locality-name>Москва</locality-name>
            <address>Яузская улица</address>
        </location>
        <sales-agent>
            <phone>8-495-589-8013</phone>
        </sales-agent>
    </offer>

</realty-feed>
    """

xmltemplate = """<?xml version="1.0" encoding="UTF-8"?>
<realty-feed xmlns="http://webmaster.yandex.ru/schemas/feed/realty/2010-06">
</realty-feed>
    """

from lxml import etree
import datetime
import time
from ..models import Flat

def gettime():
    gtime = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S{}")
    gutc = '{}{:0>2}:{:0>2}'.format('-' if time.altzone > 0 else '+', abs(time.altzone) // 3600, abs(time.altzone // 60) % 60)
    return gtime.format(gutc)


def get(queryset):
    root = etree.fromstring(xmltemplate.encode('utf-8'))

    gdate = etree.SubElement(root, 'generation-date')
    gdate.text = gettime()

    for flat in queryset:
        offer = etree.SubElement(root,'offer')
        offer.attrib['internal-id'] = flat.uid

        etree.SubElement(offer, "property-type").text = "жилая"
        etree.SubElement(offer, "category").text = "квартира"
        etree.SubElement(offer, "url").text = flat.gilkvar.site
        etree.SubElement(offer, "creation-date").text = gettime()

        location = etree.SubElement(offer, "location")
        etree.SubElement(location, "country").text = "Россия"
        etree.SubElement(location, "locality-name").text = flat.gilkvar.city
        etree.SubElement(location, "address").text = flat.gilkvar.address()

        agent = etree.SubElement(offer, "sales-agent")
        etree.SubElement(agent, "phone").text = flat.gilkvar.phone
        etree.SubElement(agent, "email").text = flat.gilkvar.email

        etree.SubElement(offer, "building-section").text = str(flat.housing)
        etree.SubElement(offer, "floor").text = str(flat.floor)
        etree.SubElement(offer, "area").text = str(flat.area)

        price = etree.SubElement(offer, "value")
        etree.SubElement(price, "value").text = str(flat.price)
        etree.SubElement(price, "currency").text = "RUR"

        if flat.balcony == Flat.YES:
            etree.SubElement(offer, "balcony").text = "0"


    return etree.tostring(root, pretty_print=True)
