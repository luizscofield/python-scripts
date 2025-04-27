from elk_request import opensearch_request

response = opensearch_request(path='/_cat/indices?v')

print(response.text)