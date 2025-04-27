from elk_request import opensearch_request

response = opensearch_request(path='/_snapshot')

print(response.text)