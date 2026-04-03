from flask import Flask, render_template, request
from sftp_logic import subir_archivo_sftp
import os

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/subir', methods=['POST'])
def subir():
    
    if 'archivo' not in request.files:
        return "<h3>No se seleccionó ningún archivo.</h3><a href='/'>Volver</a>"
    
    f = request.files['archivo']
    
    if f.filename == '':
        return "<h3>Nombre de archivo vacío.</h3><a href='/'>Volver</a>"

    
    ruta_temp = os.path.join(os.getcwd(), f.filename)
    f.save(ruta_temp)
    
    
    exito = subir_archivo_sftp(ruta_temp, f.filename)
    
    
    if os.path.exists(ruta_temp):
        os.remove(ruta_temp)
    
    
    if exito:
        return """
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1 style="color:green;">¡Archivo subido con éxito!</h1>
            <p>Se ha transferido al VPS mediante el protocolo seguro SFTP.</p>
            <a href="/">Subir otro archivo</a>
        </div>
        """
    else:
        return """
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1 style="color:red;">Error en la transferencia SFTP</h1>
            <p>Asegúrate de que el servicio SSH esté activo en el servidor.</p>
            <a href="/">Reintentar</a>
        </div>
        """

if __name__ == '__main__':
    
    app.run(debug=True, port=5000)