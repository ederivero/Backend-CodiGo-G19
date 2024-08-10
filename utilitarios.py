from math import ceil
# MIME > Multipurpose Internet Mail Extension
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Simple Mail Transfer Protocol
from smtplib import SMTP
from os import environ
from cryptography.fernet import Fernet


def serializadorPaginacion(total: int, pagina: int, porPagina: int):
    # Operador TERNARIO
    #           VAL_VERDADERO IF CONDICIONAL     ELSE VALOR_FALSO
    itemsPorPagina = porPagina if total >= porPagina else total

    # Forma tradicional
    # if total >= porPagina:
    #     itemsPorPagina = porPagina
    # else:
    #     itemsPorPagina = total

    totalPaginas = ceil(total / itemsPorPagina) if itemsPorPagina > 0 else None

    paginaPrevia = pagina - 1 if pagina > 1 and pagina <= totalPaginas else None

    paginaSiguiente = pagina + 1 if totalPaginas > 1 and pagina < totalPaginas else None

    return {
        "itemsPorPagina": itemsPorPagina,
        "totalPaginas": totalPaginas,
        "total": total,
        "paginaPrevia": paginaPrevia,
        "paginaSiguiente": paginaSiguiente,
        "porPagina": porPagina,
        "pagina": pagina
    }


def enviarCorreo(destinatario, titulo, texto, html):
    if not destinatario:
        print('Es necesario el correo')
        return

    emailEmisor = environ.get('CORREO_EMISOR')
    passwordEmisor = environ.get('PASSWORD_CORREO_EMISOR')

    # creamos el cuerpo de nuestro email
    cuerpo = MIMEText(texto, 'plain')
    cuerpoHtml = MIMEText(html, 'html')

    # ahora comenzamos a crear la configuracion de nuestro email
    correo = MIMEMultipart('alternative')
    # configuramos el titulo
    correo['Subject'] = titulo

    # los destinatarios
    correo['To'] = destinatario

    # adjuntamos el cuerpo a nuestro correo
    correo.attach(cuerpo)
    correo.attach(cuerpoHtml)

    # creamos la conexion que se encargara de realizar el envio del correo
    # 587 es el puerto estandar para todos los servidores de correos
    emisor = SMTP(environ.get('CORREO_HOST'), 587)
    emisor.starttls()

    emisor.login(emailEmisor, passwordEmisor)
    # es importante colocar la direccion del emisor y tiene que ser igual que la del login porque sino puede lanzar errores de autenticacion
    emisor.sendmail(from_addr=emailEmisor,
                    to_addrs=destinatario, msg=correo.as_string())

    emisor.quit()

    print('Correo enviado exitosamente')


def encriptarTexto(texto):
    fernet = Fernet(environ.get('FERNET_KEY'))

    textoEncriptado: bytes = fernet.encrypt(bytes(texto, 'utf-8'))

    # convertimos los byes a string
    return textoEncriptado.decode('utf-8')


def desencriptarTexto(textoEncriptado):
    print(textoEncriptado)
    fernet = Fernet(environ.get('FERNET_KEY'))

    texto = fernet.decrypt(textoEncriptado)

    return texto
