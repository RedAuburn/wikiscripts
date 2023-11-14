from bs4 import BeautifulSoup, SoupStrainer
import country_converter as coco
import requests

solidnet_members = 'http://www.solidnet.org/system/modules/org.opencms.apollo/elements/list-ajax.jsp?contentpath=/.content/lists/l_00010.xml&instanceId=li_b0568dfd&elementId=le_9261a3c1&sitepath=/links/communist-and-workers-parties/&subsite=/sites/default/&__locale=en&loc=en&option=paginate&'
results = []

print("downloading...")
raw = requests.get(solidnet_members)
print("downloaded\n")
soup = BeautifulSoup(raw.text, features="lxml")
raw_members = soup.findAll(attrs={"itemprop": "name"})

for raw_member in raw_members:
    name_tag = raw_member.find("a")
    for string in name_tag:
        val = string.get_text()
        results.append([item.strip() for item in val.split(',', 1)])

#results info
member_countries = []

for result in results:
    if result[0] not in member_countries:
        member_countries.append(result[0])

for country in member_countries:
    print(country+':')
    for item in results:
        if item[0] == country:
            print('  '+item[1])

print('\nTotal countries:', len(member_countries))
print('Total member parties:', len(results))

standard_names = coco.convert(names=member_countries, to='ISO2')
css_list = ""
for name in standard_names:
    css_list += '.'+name+', '
print(css_list[:-2].lower())
