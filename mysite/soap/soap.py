from spyne import Application, rpc, ServiceBase, Iterable
from spyne import Iterable, Array
from spyne.model.complex import XmlAttribute, ComplexModel
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.views.decorators.csrf import csrf_exempt
from spyne.model.primitive import String
from spyne.protocol.soap import Soap11
from spyne.server import django
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from django.db import IntegrityError

from mysite.models.Ubicacion import Ubicacion
from mysite.models.Elemento import Elemento

class Ubicaciones(ComplexModel):
    ubicacion = String
    nivel1 = String
    
class Elementos(ComplexModel):
    elemento1 = String
    elemento2 = String
    elemento3 = String

class HelloWorldService(ServiceBase):
    @rpc(Ubicaciones, _returns=Elementos)
    def getElements(ctx, ubiList):
        data = ubiList.as_dict()
        
        if Ubicacion.ubicacion == '' and Ubicacion.nivel1 == '':
            Elemento.elemento1 = 'Edificio1'
            Elemento.elemento2 = 'Edificio2'
            Elemento.elemento3 = 'Edificio3'
            ubiList = Elemento.objects.values('elemento1', 'elemento2', 'elemento3')
            
        return ubiList


application = Application(
    [HelloWorldService], 
    tns='django.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

def consulta():
    django_soap_app = DjangoApplication(application)
    my_soap_app = csrf_exempt(django_soap_app)
    return my_soap_app


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at:  ")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()