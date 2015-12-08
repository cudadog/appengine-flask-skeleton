"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import json
from flask import Flask, request

app = Flask(__name__)


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'I am alive'


@app.route('/api_v001', methods=['POST'])
def med_check_response():
    """Read content from Alexa"""
    content = request.get_json(silent=True)
    # import pdb; pdb.set_trace()
    # content variables
    is_new = content['session']['new']
    med = content['request']['intent']['slots']['Medicine']['value']
    # response documented here:
    # https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
    ssml_response = "<speak>You asked for %s.</speak>" % med
    url_link = 'http://www.listentoyoutube.com/middle.php?server=srv71&hash=s7DIsJ5yyqmwa3JtmJeYbGqs26Sqamq0l5eXcW5kn2NqarWEz9bXnaeE14ujqK2tyMg%253D&file=What%20is%20Open%20Source%20explained%20in%20LEGO.mp3'
    ssml_response = "<speak>You asked for %s. <audio src='%s'/></speak>" % (med, url_link)
    ssml_reprompt = "<speak>I didn't understand you. What are you looking for?</speak>"
    if med == 'aspirinx':
        should_end_session = True
    else:
        should_end_session = False
    resp = {"version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "SSML",
                        "ssml": ssml_response,
                    },
                    "reprompt": {
                        "type": "SSML",
                        "ssml": ssml_reprompt,
                    },
                    "card": {
                        "type": "Simple",
                        "title": "MedCheck",
                        "content": "Requested %s" % med
                    },
                    "shouldEndSession": should_end_session
                },
                }
    retval = json.dumps(resp)

    return retval


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
