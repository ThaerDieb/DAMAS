import urlparse

url="http://localhost:8000/en/tool/?file=paper1_Hara_checked.xml"
query = urlparse.urlparse(url)
print query
file_name =urlparse.parse_qs(query.query)['file'][0]
print file_name