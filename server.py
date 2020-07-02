
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from pprint import pprint
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://dp3060:6873@35.231.103.173/proj1part2"
#35.243.220.243

# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)
print("hello")
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace happer'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #print(request.args)


  #
  # example of a database query
  #
  #cursor = g.conn.execute("SELECT name FROM test")
  #names = []
  #for result in cursor:
    #names.append(result['name'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  actor_list=[]
  director_list=[]
  genre_list=[]
  language_list=[]
  award_list=[]
  streaming_service_list=[]	
  genre_list=[]
  actor_list.append("None") 	
  director_list.append("None")
  language_list.append("None")
  award_list.append("None")
  streaming_service_list.append("None")
  genre_list.append("None")	
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM ACTOR NATURAL JOIN PERSON ORDER BY NAME")
  for als in cursor:
  	actor_list.append(als[0])	
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM DIRECTOR NATURAL JOIN PERSON ORDER BY NAME") 	
  for dls in cursor:
  	director_list.append(dls[0])	
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM LANGUAGES ORDER BY NAME")	
  for lls in cursor:
  	language_list.append(lls[0])	
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM AWARD ORDER BY NAME")	
  for wls in cursor:
  	award_list.append(wls[0])
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM STREAMING_SERVICES ORDER BY NAME")	
  for sls in cursor:
  	streaming_service_list.append(sls[0])
  cursor =g.conn.execute("SELECT DISTINCT(NAME) FROM GENRE ORDER BY NAME")	
  for gls in cursor:
  	genre_list.append(gls[0])	
  
 
  return render_template("index.html",actor_list=actor_list,director_list=director_list,language_list=language_list,award_list=award_list,streaming_service_list=streaming_service_list,genre_list=genre_list)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/recommended_movies')
def recommended_movies():
  cursor =g.conn.execute("SELECT NAME,WATCHABLE_LIST_ID FROM WATCHABLE_LIST")
  pairs = []
  for result in cursor:
    #names.append(result['name'])  # can also be accessed using result[0]
    pairs.append(result)
    print(result[0])
  cursor=g.conn.execute("SELECT NAME,STREAMING_SERVICES_ID FROM STREAMING_SERVICES")  
  streaming_services = []
  for record in cursor:
    #names.append(result['name'])  # can also be accessed using result[0]
    streaming_services.append(record)
  cursor.close()
  context=dict(data=pairs)
  return render_template("recommended_movies.html",movie_list=pairs,streaming_service_list=streaming_services)

@app.route('/more_details')
def more_details():
 
  return render_template("more_details.html")
  
@app.route('/movie_details',methods=['POST','GET'])
def movie_details():
  ids=[]	
  details=dict()
  actor_details=[]
  director_details=[]
  genre_details=[]
  language_details=[]
  streaming_service_details=[]
  award_details=[]
  title=request.form['title'].lower()		
  #cursor =g.conn.execute("SELECT * FROM WATCHABLE_LIST,ACTED,DIRECTED,BELONGS_TO,AVAILABLE_IN,IS_AVAILABLE_ON WHERE ACTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND DIRECTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND BELONGS_TO.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND AVAILABLE_IN.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND WATCHABLE_LIST.WATCHABLE_LIST_ID=IS_AVAILABLE_ON.WATCHABLE_LIST_ID AND LOWER(NAME) LIKE '%%"+title+"%%'")
  cursor =g.conn.execute("SELECT * FROM WATCHABLE_LIST WHERE LOWER(NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
  	details['movie_name']=result[1]
  	details['country_of_origin']=result[2]
  cursor =g.conn.execute("SELECT PERSON.NAME FROM WATCHABLE_LIST,ACTED,PERSON WHERE ACTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND ACTED.PERSON_ID=PERSON.PERSONID AND LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
   	actor_details.append(result[0])
  cursor =g.conn.execute("SELECT PERSON.NAME FROM WATCHABLE_LIST,DIRECTED,PERSON WHERE DIRECTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND DIRECTED.PERSON_ID=PERSON.PERSONID AND LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
    director_details.append(result[0])
  cursor =g.conn.execute("SELECT GENRE.NAME FROM GENRE,BELONGS_TO,WATCHABLE_LIST WHERE GENRE.GENRE_ID=BELONGS_TO.GENRE_ID AND BELONGS_TO.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
    genre_details.append(result[0])
  cursor =g.conn.execute("SELECT LANGUAGES.NAME FROM  LANGUAGES,AVAILABLE_IN,WATCHABLE_LIST WHERE LANGUAGES.LANGUAGE_ID=AVAILABLE_IN.LANGUAGE_ID AND AVAILABLE_IN.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
    language_details.append(result[0])
  cursor =g.conn.execute("SELECT AWARD.NAME FROM  AWARD NATURAL JOIN WATCHABLE_LIST WHERE  LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
    award_details.append(result[0])
  cursor =g.conn.execute("SELECT STREAMING_SERVICES.NAME FROM STREAMING_SERVICES,IS_AVAILABLE_ON,WATCHABLE_LIST WHERE STREAMING_SERVICES.STREAMING_SERVICES_ID=IS_AVAILABLE_ON.STREAMING_SERVICES_ID AND IS_AVAILABLE_ON.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND LOWER(WATCHABLE_LIST.NAME) LIKE '%%"+title+"%%'")
  for result in cursor:
    streaming_service_details.append(result[0])

  cursor.close()
  return render_template("movie_details.html",details=details,actor_details=actor_details,director_details=director_details,genre_details=genre_details,language_details=language_details,streaming_service_details=streaming_service_details,award_details=award_details)

  

  
@app.route('/getresults',methods=['POST'])
def getresults():
  liked_watchable_list_ids_m=[]
  disliked_watchable_list_ids_m=[]
  streaming_services_id_m=[]
  liked_watchable_list_ids = request.form.getlist("Like")
  disliked_watchable_list_ids = request.form.getlist("Dislike")
  streaming_services_id = request.form.getlist("Streamlist")
  
  for i in liked_watchable_list_ids:
  	i= int(i)
  	liked_watchable_list_ids_m.append(i)
  print("liked_watchable_list_ids_m",liked_watchable_list_ids_m)	
  
  for j in disliked_watchable_list_ids:
  	j= int(j)
  	disliked_watchable_list_ids_m.append(j)
  print("disliked_watchable_list_ids_m",disliked_watchable_list_ids_m)	
  
  for k in streaming_services_id:
  	k= int(k)
  	streaming_services_id_m.append(k)
  print("streaming_services_id_m",streaming_services_id_m)	
  
  print(liked_watchable_list_ids_m)
  print(disliked_watchable_list_ids_m)
  print(streaming_services_id_m)
   ## Recommendation Logic writen below remove and put it at right place after this
  query = "SELECT * FROM WATCHED"
  cursor = g.conn.execute(query)
  results=[]
    #print (cursor)
  user={"liked":[1,3,8,9,13,15],"disliked":[4,5,6],"streaming_service":[]}
  user["liked"]=liked_watchable_list_ids_m
  user["disliked"]=disliked_watchable_list_ids_m
  user["streaming_service"]=streaming_services_id_m
  comb=dict()
  for result in cursor:
      #print ("OK")
      print (result)
      if (int(result[1]) not in comb):
        comb[int(result[1])]=[]
        if (result[0]):
           comb[int(result[1])].append(int(result[2]))
      else :
        if (result[0]):
           comb[int(result[1])].append(int(result[2]))
  pprint (comb)
  show=set()
  inter=""
  for key,value in comb.items():
    cnt=0
    for i in user["liked"]:
      if (i in value):
        cnt+=1
    if (cnt):
      for i in value:
        if (i not in user["liked"] and i not in user["disliked"]):
          show.add(i)
  print (show)
  if (show):
    sho=""
    for i in show:
      sho=sho+str(i)+","
    sho=sho[:-1]
    inter="((SELECT NAME FROM IS_AVAILABLE_ON,WATCHABLE_LIST WHERE IS_AVAILABLE_ON.AVAILABLE_FOR_FREE AND IS_AVAILABLE_ON.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID))"
    query="(SELECT NAME FROM WATCHABLE_LIST WHERE WATCHABLE_LIST_ID IN ("+sho+")) INTERSECT "
    if (len(user["streaming_service"])):
      ss=""
      for i in user["streaming_service"]:
        ss=ss+str(i)+","
      ss=ss[:-1]
      inter=inter[:-1]+"UNION (SELECT NAME FROM IS_AVAILABLE_ON,WATCHABLE_LIST WHERE NOT IS_AVAILABLE_ON.AVAILABLE_FOR_FREE AND IS_AVAILABLE_ON.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND IS_AVAILABLE_ON.STREAMING_SERVICES_ID IN ("+ss+")))"
    query=query+inter
    cursor = g.conn.execute(query)
    print (query)
    results=[]
    for result in cursor:
      results.append(result['name'])
    print (results)
    context=dict(data=results)
  else :
    context = dict()
  return render_template("results.html",**context)	
  
# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

@app.route('/submit', methods=['POST'])
def submit():
  print ("Inside Submit")
  return
  
@app.route('/retrieve', methods=['POST','GET'])
def retrieve():
  actor=request.form['actor']
  if actor== "None":
  	actor=''
  
  director=request.form['director']
  
  if director== "None":
  	director=''
   
  
  genre=request.form['genre']

  if genre== "None":
  	genre=''
  
  
  lang=request.form['language']
  
  if lang== "None":
  	lang=''
  
  
  award=request.form['award']
  
  if award== "None":
  	award=''
  
  streaming_service=request.form['streaming service']
  
  if streaming_service== "None":
  	streaming_service=''
  
  
  query = "SELECT * FROM WATCHABLE_LIST"
  #query = "SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM LANGUAGES,AVAILABLE_IN,WATCHABLE_LIST WHERE LANGUAGES.NAME LIKE '%%English%%'"
  #query = "SELECT * FROM STREAMING_SERVICES"
  sub_query=''
  if actor != '' or director != '' or genre !='' or lang !='' or award!='' or streaming_service!='' :
  	#query=query+" WHERE NAME IN "
  	
  	if actor!='':
  		actor_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM PERSON,ACTED,WATCHABLE_LIST WHERE PERSON.PERSONID=ACTED.PERSON_ID AND ACTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND PERSON.NAME LIKE '%%"+actor+"%%')"
  		sub_query=sub_query+actor_sub_query
  	if director!='':
  		director_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM PERSON,DIRECTED,WATCHABLE_LIST WHERE PERSON.PERSONID=DIRECTED.PERSON_ID AND DIRECTED.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND PERSON.NAME LIKE '%%"+director+"%%')"
  		if sub_query=='':
  			sub_query=sub_query+director_sub_query
  		else:
  			sub_query=sub_query+" INTERSECT "+director_sub_query
  	if genre!='':
  		genre_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM GENRE,BELONGS_TO,WATCHABLE_LIST WHERE GENRE.GENRE_ID=BELONGS_TO.GENRE_ID AND BELONGS_TO.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND GENRE.NAME LIKE '%%"+genre+"%%')"
  		if sub_query=='':
  			sub_query=sub_query+genre_sub_query
  		else:
  			sub_query=sub_query+" INTERSECT "+genre_sub_query
  	if lang!='':
  		lang_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM LANGUAGES,AVAILABLE_IN,WATCHABLE_LIST WHERE LANGUAGES.LANGUAGE_ID=AVAILABLE_IN.LANGUAGE_ID AND AVAILABLE_IN.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND LANGUAGES.NAME LIKE '%%"+lang+"%%')"
  		if sub_query=='':
  			sub_query=sub_query+lang_sub_query
  		else:
  			sub_query=sub_query+" INTERSECT "+lang_sub_query
  	if award!='':
  		award_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM AWARD,WATCHABLE_LIST WHERE AWARD.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND AWARD.NAME LIKE '%%"+award+"%%')"
  		if sub_query=='':
  			sub_query=sub_query+award_sub_query
  		else:
  			sub_query=sub_query+" INTERSECT "+award_sub_query
  	if streaming_service!='':
  		streaming_service_sub_query="(SELECT DISTINCT(WATCHABLE_LIST.NAME) FROM STREAMING_SERVICES,IS_AVAILABLE_ON,WATCHABLE_LIST WHERE STREAMING_SERVICES.STREAMING_SERVICES_ID=IS_AVAILABLE_ON.STREAMING_SERVICES_ID AND IS_AVAILABLE_ON.WATCHABLE_LIST_ID=WATCHABLE_LIST.WATCHABLE_LIST_ID AND STREAMING_SERVICES.NAME LIKE '%%"+streaming_service+"%%')"
  		if sub_query=='':
  			sub_query=sub_query+streaming_service_sub_query
  		else:
  			sub_query=sub_query+" INTERSECT "+streaming_service_sub_query
  	query=query
  
  #print(query)
  #query="SELECT * FROM WATCHABLE_LIST WHERE NAME LIKE (SELECT WATCHABLE_LIST.NAME FROM LANGUAGES NATURAL JOIN AVAILABLE_IN NATURAL JOIN WATCHABLE_LIST WHERE LANGUAGES.NAME LIKE '%%ENGLISH%%')"
  #query="SELECT * FROM LANGUAGES WHERE NAME LIKE '%%English%%'"
  if (sub_query):
    #sub_query=sub_query[1:-1]
    print (sub_query)
    cursor = g.conn.execute(sub_query)
    results=[]
    #print (cursor)
    for result in cursor:
      #print ("OK")
      results.append("'"+result['name']+"'")
      #print (result['name'])
    if results:
      query=query + " WHERE NAME LIKE "
      for result in results:
        query = query + result + " OR NAME LIKE "
      query=query[:-13]
      print (query)
      cursor = g.conn.execute(query)
      results=[]
      for result in cursor:
        results.append(result['name'])
        print(result)  # can also be accessed using result[0]
      cursor.close()
      context = dict(data = results)
    else :
      context = dict()
  else: 
    cursor = g.conn.execute(query)
    results=[]
    for result in cursor:
      results.append(result['name'])
      print(result['name'])  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = results)
  return render_template("index2.html", **context)

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
