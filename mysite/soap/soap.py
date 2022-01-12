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
from spyne.protocol.json import JsonDocument
from spyne.server import django
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from django.db import IntegrityError
from spyne import Mandatory as M

class Ubicaciones(ComplexModel):
    centro = Unicode
    nivel1 = Unicode
    nivel2 = Unicode
    nivel3 = Unicode
    nivel4 = Unicode
    nivel5 = Unicode
    nivel6 = Unicode
    
class Resultados(ComplexModel):
    type = Unicode
    code = Double
    message = Unicode
    
class Datos(ComplexModel):
    descripcion = Unicode
    codigo = Unicode
    
class Elementos(ComplexModel):
    elementos = M(Array(M(Datos, maxOccurs='unbounded', wrapped = False), member_name='elemento'))
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
            elements.elementos = [["Area1", "1001"], ["Area2", "1002"], ["Area3", "1003"]]
        elif codUbicacion.nivel1 == "":
            #for i in range(1, 4):
            elements.elementos = [["Hospital1", "H01"], ["Hospital2", "H02"], ["Hospital3", "H03"]]
        elif codUbicacion.nivel2 == "":
            #for i in range(1, 4):
            elements.elementos = [["Edificio1", "E01"], ["Edificio2", "E02"], ["Edificio3", "E03"]]
        elif codUbicacion.nivel3 == "":
            #for i in range(1, 4):
            elements.elementos = [["Planta1", "P01"], ["Planta2", "P02"], ["Planta3", "P03"]]
        elif codUbicacion.nivel4 == "":
            elements.elementos = [["Unidad1, Ala1", "U01"], ["Unidad2, Ala2", "U02"], ["Unidad2, Ala2", "U02"]]
        elif codUbicacion.nivel5 == "":
            elements.elementos = [["Sala1, Zona1", "S01"], ["Sala2, Zona2", "S02"], ["Sala3, Zona3", "S03"]]
        elif codUbicacion.nivel6 == "":
            elements.elementos = [["Sala1, Habitacion1", "H01"], ["Sala2, Habitacion2", "H02"], ["Sala3, Habitacion3", "H03"]]

        return elements
            

application = Application(
    [UbicacionesService], 
    tns='django.examples.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=JsonDocument())

wsgi_application = WsgiApplication(application)

def consulta():
    django_soap_app = DjangoApplication(application)
    my_soap_app = csrf_exempt(django_soap_app)
    return my_soap_app


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.json.JsonDocument').setLevel(logging.DEBUG)
    #spyne.protocol.xml

    logging.info("Servidor conectado en http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/soap/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()