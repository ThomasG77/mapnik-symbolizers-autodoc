#!/usr/bin/env python

try:
    # <= python 2.5
    import simplejson as json
except ImportError:
    # >= python 2.6
    import json


def getCamelCase(s, sep=' ', lower = False):
    """ Transform to camelcase, optionnal separator sep and optionnal lower to set first letter to lowercase
    >>> getCamelCase("my-beautiful-function", "-", True)
    'myBeautifulFunction'
    """
    return ''.join([t.title() for t in s.split(sep)])

# Get raw reference.json from https://raw.github.com/mapnik/reference.json/master/reference.json
reference = json.load(open('reference.json','r'))

# Get all columns for each symbolizer
symbolizersHeaders = []
for i,j in reference.iteritems():
    if i=='symbolizers':
        for k,l in j.iteritems():
                # Exclude map object
                if k != 'map':
                    # Loop to get symbolizer name
                    uniqueProperties = []
                    # Loop to get symbolizers properties
                    for m, n in l.iteritems():
                        propertyList =[]
                        for o,p in n.iteritems():
                            propertyList.append(str(o))
                            # Retrieve unique keys for unique fields of each symbolizers properties
                            uniqueProperties.extend(propertyList)
                    #Common columns per symbolizers
                    # Get in unique objet, the symbolizer name, unique properties for building table and dictionnary for each symbolisers
                    symbolizersHeaders.append((getCamelCase (k + "-"+ i, '-'), list(set(uniqueProperties)), l))



# Now time to input in Jinja2
from jinja2 import Template
template = Template('{% for symbolizer in symbolizerContent %}\
{# Symbolizer title #}\
{{ symbolizer[0] }}\n\
\
{# Symbolizer header #}\
|parameter|{{ symbolizer[1]|join("|") }}|\n\
{# separator for markdown table #}\
|---------\
{% for symDescript in symbolizer[1] %}\
|{{ "-" * symDescript|length }}\
{% endfor %}\
|\n\
{% for k,v in symbolizer[2].iteritems() %}\
{# Get parameter name #}\
|{{ k }}\
{# Loop to get mapping between columns and data #}\
{% for symDescript in symbolizer[1] %}\
{% for k1,v1 in v.iteritems() if k1==symDescript%}\
{# Do not find building function to check if type = list so an alternative #}\
{% if v1 is iterable and v1 is not string %}\
|{{ v1|join(",") }}\
{% else %}\
|{{ v1 }}\
{% endif %}\
{% else %}\
{# No mapping, so empty #}\
|\
{% endfor %}\
\
{% endfor %}\
|\n\
{% endfor %}\
\n\
{% endfor %}')
result = template.render(symbolizerContent=symbolizersHeaders)
f = open('/tmp/jinja.txt', 'w')
f.write(result)
f.close()

