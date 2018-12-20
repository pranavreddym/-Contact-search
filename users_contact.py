from flask import Flask, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from pprint import pprint
import json


app = Flask(__name__)

awsauth = AWS4Auth('*****', '*****', 'us-east-1', 'es')

es = Elasticsearch(
	hosts=[{'host': 'search-eai-os63j4l7hdeghsozuu7xwyfejm.us-east-1.es.amazonaws.com', 'port': 443}],
	http_auth=awsauth,
	use_ssl=True,
	verify_certs=True,
	connection_class=RequestsHttpConnection
)
pprint(es.info())
# es.indices.delete(index='users', ignore=[400, 404])

def search_contact(name):
    result = es.search(q=name)
    print('>>>>>Result of the search function<<<<<')
    total_number_of_users = result['hits']['total']
    if total_number_of_users == 0:
        return True, None;
    else:
        id = result['hits']['hits'][0]['_id']
        return False, id

@app.route('/')
def default_method():
    return "Welcome to the application"

@app.route('/contact/', methods=['GET'])
def get_all_contacts():
    print("Inside Get All Contacts")
    page_size = request.args.get('pageSize', default='*', type=str)
    page = request.args.get('page', default='*', type=str)
    search_term = request.args.get('query', default='*', type=str)

    if page_size == '*' or page_size == '':
        res_size = 10
    else:
        res_size = int(page_size)

    if page == '*' or page == '' or int(page) == 1:
        offset = 0
    else:
        offset = res_size * (int(page) - 1)

    if search_term == '*' or search_term == '':
        query = json.dumps({
            "query": {
                "match_all": {}
            }
        })
    else:
        query = json.dumps({
            "query": {
                "query_string": {"default_field": "name", "query": "*" + search_term + "*"}
            }
        })

    print("page_size={} page={} search_term={}".format(page_size, page, search_term))
    print("offset={} query={}".format(offset, query))

    search_results = []
    res = es.search(index="users", body=query, size=res_size, from_=offset)
    for hit in res['hits']['hits']:
        search_results.append(hit["_source"])
    if search_results:
        return json.dumps({'results': search_results})
    else:
        return "No results found"


@app.route('/contact/<name>', methods=['GET'])
def get_contact(name):

    result = es.search(q=name)
    print("inside the get function")
    users = result['hits']['total']
    if users == 0:
        return json.dumps({'Success':False, 'message': 'User not found'}, 200, {'Content-Type':False})

    body = result['hits']['hits'][0]['_source']
    return json.dumps({'Success':True, 'Body':body})

@app.route('/contact/<name>', methods=['PUT'])
def update_contact(name):

    print("inside the update method")
    flag, id = search_contact(name)
    if flag:
        return json.dumps({'success': False, 'message': 'Sorry, the requested user doesn\'t exists'}, 200,
                          {'ContentType': 'application/json'})

    user_data = request.json

    if 'contact' not in user_data:
        return json.dumps({'success':False, 'message': 'contact of the person not found'}, 200, {'ContentType': 'application/json'})

    data = {}
    data['name'] = name
    data['contact'] = user_data['contact']
    update_result = es.index(index="users", doc_type='user-detail', id=id, body=data)
    print(">>>>>Result from the update function")
    pprint(update_result)
    return json.dumps({'success': True}, 200, {'ContentType': 'application/json'})

@app.route('/contact/<name>', methods=['DELETE'])
def delete_contact(name):

    print('inside the delete contact method')
    flag, id = search_contact(name)

    if flag:
        return json.dumps({'success': False, 'message': 'Sorry, the requested user doesn\'t exists'}, 200,
                          {'ContentType': 'application/json'})

    delete_result = es.delete(index='users', doc_type='user-detail', id=id)
    if delete_result['_shards']['successful'] == 1:
        return json.dumps({'success' : True}, 200, {'ContentType':'application/json'})

    return json.dumps({'success':False, 'message':'Something went wrong'}, 200, {'Content-Type':'application/json'})

@app.route('/contact', methods = ['POST'])
def add_contact():

    print(">>>>>Entered the add contact method<<<<<<")
    try:
        count_of_users = es.count(index="users")['count']
    except:
        print('creating first user')
        count_of_users = 0;


    print("count of users " + str(count_of_users))
    count_of_users += 1
    print("data = ", request)
    users_data = request.json
    print(users_data)

    # Handling if the structure of the input data is not appropriate
    if not users_data or 'name' not in users_data or 'contact' not in users_data:
        return json.dumps({'success': False, 'message': 'The body should contain name and contact keys'}, 200,
                          {'ContentType': 'application/json'})
    print(type(users_data))
    print(users_data)
    name = users_data["name"]
    unique_user = False
    if name :
        unique_user,id = search_contact(name)
    else:
        return json.dumps({'success': False, 'message': 'Parameter name and contact should contain values'}, 200,
                          {'ContentType': 'application/json'})

    print("unique user > ", unique_user)
    if not unique_user:
        return json.dumps({'success': False, 'message': 'Sorry, the user already exists'}, 200,
                          {'ContentType': 'application/json'})

    data = {}
    data['name'] = users_data['name']
    data['contact'] = users_data['contact']

    result = es.index(index="users", doc_type='user-detail', id=count_of_users, body=data)

    if result['_shards']['successful'] == 1:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False, 'message' : 'Something went wrong'}, 200, {'ContentType' : 'application/json'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)