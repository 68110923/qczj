# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
s='导演:中岛哲也TetsuyaNakashima主演:松隆子TakakoMatsu/冈田将生...'
import re

print(re.sub('[a-zA-Z0-9\./]', '', s))