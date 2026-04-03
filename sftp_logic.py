import paramiko
import os

def subir_archivo_sftp(ruta_local, nombre_destino):
    """
    Función para transferir archivos de forma segura 
    desde el cliente (Flask) hacia el servidor SFTP.
    """
    
    
    host = "127.0.0.1" 
    puerto = 2222
    usuario = "antonella"  
    clave = "password"     

    ssh = None
    try:
        
        ssh = paramiko.SSHClient()
        
        
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
       
        print(f"Conectando a {host} vía SFTP...")
        ssh.connect(host, port=puerto, username=usuario, password=clave, timeout=10)

        
        sftp = ssh.open_sftp()
        
       
        ruta_remota = f"/var/sftp/uploads/{nombre_destino}"
        
        
        sftp.put(ruta_local, ruta_remota)
        
        
        sftp.close()
        ssh.close()
        print("Transferencia SFTP completada con éxito.")
        return True

    except Exception as e:
        
        print(f"Error crítico en la conexión SFTP: {e}")
        if ssh:
            ssh.close()
        return False