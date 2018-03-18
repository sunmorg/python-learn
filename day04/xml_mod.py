# -*- coding:utf-8 -*-
# Author：sunmorg

import xml.etree.ElementTree as ET

tree = ET.parse("xml_test")

root = tree.getroot()

print(root.tag)

# for child in root:
#     print("......",child.tag,child.attrib)
#     for i in child:
#         print(i.tag,i.text)


# for node in root.iter('year'):
#     print(node.tag,node.text)

# for node in root.iter('year'):
#     new_year = int(node.text) + 1
#     node.text = str(new_year)
#     node.set("update","yes")
#
# tree.write("xml_test")

for country in root.findall("country"):
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)

tree.write('output.xml')