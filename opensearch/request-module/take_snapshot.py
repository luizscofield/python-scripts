from elk_request import opensearch_request

bucket = "bucket-name"
snapshot_name = 'snapshot-name'

payload = {
  "indices": "*",
  "ignore_unavailable": True,
  "include_global_state": False
}

response = opensearch_request(
    method  = 'PUT', 
    path    = f'/_snapshot/{bucket}/{snapshot_name}?wait_for_completion=true',
    payload = payload
)

print(response.text)