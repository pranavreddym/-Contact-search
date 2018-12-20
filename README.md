# -Contact-search
This is a RESTFUL API for an address Book with an ElasticSearch data store

A RESTful API is one that exposes it's iterface over HTTP, and follows standard convetion for how dat should be retrieved.

The format of the data that should be send be **application/json** and should be of this format:
  \n{
  "name": {name},
  "contact": {contact}
  }
  
  The application used AWS [ElasticSearch](https://aws.amazon.com/elasticsearch-service/) as its data store. 
  The RESTful services is implemented by [flask](http://flask.pocoo.org/).
  The unittests library used is [unittest.py](https://docs.python.org/3/library/unittest.html)
  
  ## API Definitons
  
  # GET /contact?pagesize={}&page={}&query={}
    This end will help providing all the contacts for the defined defined page size, page and gfor the given query.
  # POST /contact
    This end point will create a unique contact if provided in the required format.
  # GET /contact/{name}
    This end point will return the contact by a unique name
  # PUT /contact/{name}
    This end point will be responsible for updating the contact by a unique name.
  # DELETE /contact/{name}
    This end pint shoudl delete the contact by a unique name.
   
   ## Testability
    The application build is tested with unittest.py package.
    


## How to run the application:
  
  You should have python3 installed on your machine.
  
  Just create an AWS Elastic search account and replace the access keys and end with your credentials.
  
  Run the application and enjoy the commands!
  
  
