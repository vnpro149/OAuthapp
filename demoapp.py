from flask import Flask,redirect,request,url_for
from authlib.integrations.requests_client import OAuth2Session
import json

app= Flask(__name__)
app.secret_key='hello'
client_id="76b0e49a77257d93374f"
client_secret="17c160cbbcae3052d2855aee7ff58560a6ce0051"
client=OAuth2Session(client_id=client_id,client_secret=client_secret)
code=''
state=''
hostcallback='http://localhost:5050/callback'
@app.route('/')
def indext():
    return "Hello Everyone1"
@app.route('/test')
def test():
    return "Ham test"


@app.route('/login')
def login():
    urllogin='https://github.com/login/oauth/authorize'
    uri,state=client.create_authorization_url(urllogin)
    return redirect(uri)
@app.route('/callback')
def callback():
    global code, state
    code=request.args['code']
    state=request.args['state']
    # return code
    redirecturl=url_for('fetch_token',_external=True)
    return redirect(redirecturl)

@app.route('/fetch_token')
def fetch_token():
    try:
        callbackurl=hostcallback+"?code={}&state={}".format(code,state)
        print( callbackurl)
        urltoken='https://github.com/login/oauth/access_token'
        resp=client.fetch_token(urltoken,authorization_response=callbackurl)
        print(resp['access_token'])
        # return resp
        redirecturl=url_for('user',_external=True)
        return redirect(redirecturl)
    except:
        redirecturl=url_for('login',_external=True)
        print(redirecturl)
        return redirect(redirecturl)


@app.route('/user')
def user():
    try:
        resp=client.get('https://api.github.com/user',\
                        headers={'Authorization':'Bearer OAUTH-TOKEN'})
        redirecturl=url_for('indext',_external=True)
        print(redirecturl)
        return redirect(redirecturl)
    except:
        redirecturl=url_for('login',_external=True)
        print(redirecturl)
        return redirect(redirecturl)
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)

