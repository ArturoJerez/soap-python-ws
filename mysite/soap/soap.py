from lxml.builder import ElementMaker
from spyne import Application, rpc, ServiceBase, Iterable
from spyne import Iterable, Array, Unicode
from spyne.model.complex import XmlAttribute, ComplexModel
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.views.decorators.csrf import csrf_exempt
from spyne.model.primitive import String
from spyne.model.primitive.number import Double
from spyne.protocol.soap import Soap11
from spyne.server import django
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from django.db import IntegrityError
from spyne import Mandatory as M

from mysite.models.Ubicacion import Ubicacion
from mysite.models.Elemento import Elemento

class Ubicaciones(ComplexModel):
    centro = String
    nivel1 = String
    nivel2 = String
    nivel3 = String
    nivel4 = String
    nivel5 = String
    nivel6 = String
    
class Elementos(ComplexModel):
    elementos = M(Array(M(Unicode), member_name='elemento'))

class UbicacionesService(ServiceBase):
    @rpc(Ubicaciones, _returns=Elementos)
    def getElements(ctx, codUbicacion: Ubicaciones):
        if codUbicacion.centro == "" and codUbicacion.nivel1 == "":
            elements = Elementos()
            elements.elementos = ['edificio1', 'edificio2', 'edificio3']
            return elements

application = Application(
    [UbicacionesService], 
    tns='django.examples.soap',
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

    logging.info("Servidor conectado en http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/soap/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()