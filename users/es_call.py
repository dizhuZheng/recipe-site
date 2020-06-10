from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

def esearch(username="", gender="", address="", email="", photo=""):
    client = Elasticsearch()
    q = Q("bool", should=[Q("match", username=username), Q("match", photo=photo), Q("match", address=address), Q("match", email=email), Q("match", gender=gender)], minimum_should_match=1)
    s = Search(using=client, index="users").query(q)[0:20]
    response = s.execute()
    search = get_results(response)
    return search


def get_results(response):
    results = []
    for hit in response:
        result_tuple = (hit.username, hit.gender, hit.email, hit.address, hit.photo)
        results.append(result_tuple)
    return results
