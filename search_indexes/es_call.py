from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


def esearch():
    client = Elasticsearch()
	q = Q("bool", should=[Q("match", firstname=firstname),
	Q("match", gender=gender)], minimum_should_match=1)
	s = Search(using=client, index="bank").query(q)[0:20]
	response = s.execute()
	#print("%d hits found." % response.hits.total)
	search = get_results(response)
	return search


def get_results(response):
	results = []
	for hit in response:
		result_tuple = (hit.firstname + ' ' + hit.lastname, hit.email, hit.gender, hit.address)
		results.append(result_tuple)
	return results
