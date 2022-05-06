import sys
from os import listdir
from os.path import isfile, join
import requests
import json

response = requests.get('https://api.upstash.com/v2/kafka/clusters', auth=(sys.argv[2], sys.argv[3]))
cluster_id = json.loads(response.content)[0].get('cluster_id')
response = requests.get('https://api.upstash.com/v2/kafka/topics/'+cluster_id , auth=(sys.argv[2], sys.argv[3]))

topic_list = [topic_infos.get('topic_name').replace('-','').lower() for topic_infos in json.loads(response.content)]

onlyfiles = [f for f in listdir(sys.argv[1]) if (isfile(join(sys.argv[1], f)) & f.endswith(".html"))]

mainpage_template="""# Mimir interface catalog

## Available stream data

{}

## Available Soon
(Declared in the registry but no associated topic yet.)

{}

## Not registered schema
(Existing topic that does not match any schema name)

{}

### Support or Contact

[Issues](https://github.com/indyMccarthy/Mimir-interface-doc/issues)
"""
# Declared on registry and topic name associated
schema_available_list=""
schema_available_soon=""
schema_not_registered=""

for f in onlyfiles:
    if f.rsplit('.html', 1)[0].lower() in topic_list:
        schema_available_list += '- [{}]({})\n'.format(f.rsplit('.html', 1)[0], 'schemas/{}'.format(f))
        topic_list.remove(f.rsplit('.html', 1)[0].lower())
    else:
        schema_available_soon += '- [{}]({})\n'.format(f.rsplit('.html', 1)[0], 'schemas/{}'.format(f))

for t in topic_list:
    schema_not_registered += '- {}\n'.format(t)
    

readme=mainpage_template.format(schema_available_list, schema_available_soon, schema_not_registered)

print(readme)