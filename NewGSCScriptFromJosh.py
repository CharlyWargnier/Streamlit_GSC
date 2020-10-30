import searchconsole
import streamlit as st

from apiclient import discovery
from google_auth_oauthlib.flow import Flow


st.title("Google OAuth2 flow")

st.header("Load credentials")

# Alternatively a user could upload a file with their credentials and you
# could use `Flow.from_client_secrets_file`.
client_id = st.text_input("Client ID")
client_secret = st.text_input("Client secret")


st.write("https://www.tatielou.co.uk/")

webproperty_box = st.text_input("webproperty")


credentials = {
    "installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uris": [],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
flow = Flow.from_client_config(
    credentials,
    scopes=['https://www.googleapis.com/auth/webmasters.readonly'],
    #redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'    
)


auth_url, _ = flow.authorization_url(prompt='consent')
st.write(auth_url)
code = st.text_input('Code')

flow.fetch_token(code=code)
credentials = flow.credentials

service = discovery.build(
    serviceName='webmasters',
    version='v3',
    credentials=credentials,
    cache_discovery=False,
)


account = searchconsole.account.Account(service, credentials)

###############


#account = searchconsole.authenticate(client_config='client_secrets.json')
#webproperty = account['https://www.example.com/']


#webproperty = account['https://www.tatielou.co.uk/']

webproperty = account[webproperty_box]

report = webproperty.query.range('today', days=-7).dimension('query').get()

st.write(report.rows)


