
from microWebSrv import MicroWebSrv
import ujson


@MicroWebSrv.route('/state.json', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	#formData  = httpClient.ReadRequestPostedFormData()
	#firstname = formData["firstname"]
	#lastname  = formData["lastname"]

	test= {
		"temp":27,
		"mois":70,
		"lev":40,
		"inputChannels":10,

		"plants":[{
		"valve":0,
		"art":"Minze",
		"mois":60,
		"maxmois":80,
		"consump":5,
		"mode":0,
		"analogin":3

		},{
		"valve":1,
		"art":"Minzejj",
		"mois":50,
		"maxmois":80,
		"consump":5,
		"mode":1,
		"analogin":3
		}]

		}

	content   = ujson.dumps(test)


	 #% ( MicroWebSrv.HTMLEscape(firstname),
		 #   MicroWebSrv.HTMLEscape(lastname) )
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "application/json",
								  contentCharset = "UTF-8",
								  content 		 = content )



@MicroWebSrv.route('/updateValve', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :

	dicobj=httpClient.ReadRequestContentAsJSON();
	
	#print(dicobj["art"]);



	content =" "

	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

routeHandlers = [

	( "/",	"POST",	_httpHandlerTestPost )
]

srv = MicroWebSrv(webPath='/')

srv.Start()

# ----------------------------------------------------------------------------
