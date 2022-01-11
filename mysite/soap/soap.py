from os import name
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

class Ubicaciones(ComplexModel):
    centro = Double
    nivel1 = String
    nivel2 = String
    nivel3 = String
    nivel4 = String
    nivel5 = String
    nivel6 = String
    
class Resultados(ComplexModel):
    type = String
    code = Double
    message = String
    
class Datos(ComplexModel):
    descripcion = Unicode
    codigo = Unicode
    
class Elementos(ComplexModel):
    elementos = M(Array(M(Datos), member_name='elemento'))
    ex_result = Resultados

class UbicacionesService(ServiceBase):
    @rpc(Ubicaciones, _returns=Elementos)
    def getElements(ctx, codUbicacion: Ubicaciones):
        elements = Elementos()
        elements.ex_result = Resultados()
        elements.ex_result.type = "S"
        elements.ex_result.code = 000
        elements.ex_result.message = "Proceso realizado con éxito"
        
        if codUbicacion.centro == "":
            elements.elementos = ['centro1', 'centro2', 'centro3']
            return elements
        elif codUbicacion.nivel1 == "":
            elements.elementos = ['hospital1', 'hospital2', 'hospital3']
            return elements
        elif codUbicacion.nivel2 == "":
            for i in range(1, 4):
                elements.elementos = [["Edificio"+str(i), "E0"+str(i)]]
            return elements
        elif codUbicacion.nivel3 == "":
            elements.elementos = ['planta1', 'planta2', 'planta3']
            return elements
        elif codUbicacion.nivel4 == "":
            elements.elementos = ['unidad1, ala1', 'unidad2, ala2', 'unidad3, ala3']
            return elements
        elif codUbicacion.nivel5 == "":
            elements.elementos = ['sala1, zona1', 'sala2, zona2', 'sala3, zona3']
            return elements
        elif codUbicacion.nivel6 == "":
            elements.elementos = ['sala1, habitacion1', 'sala2, habitacion2', 'sala3, habitacion3']
            return elements
        else:
            return codUbicacion
            

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