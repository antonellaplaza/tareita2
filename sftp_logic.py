import paramiko
import os

def subir_archivo_sftp(ruta_local, nombre_destino):
    """
    Función para transferir archivos de forma segura 
    desde el cliente (Flask) hacia el servidor SFTP.
    """
    
    # --- CONFIGURACIÓN DEL SERVIDOR SEGURO (VPS) ---
    # En GitHub Codespaces usamos localhost (127.0.0.1) 
    # porque el servicio SSH corre en el mismo contenedor.
    host = "127.0.0.1" 
    puerto = 22
    usuario = "antonella"  # Usuario que creamos en la terminal
    clave = "password"     # Contraseña que asignamos con chpasswd

    ssh = None
    try:
        # 1. Creamos el cliente SSH
        ssh = paramiko.SSHClient()
        
        # 2. Política para aceptar claves de host desconocidas (necesario en entornos de prueba)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 3. Establecemos la conexión segura
        print(f"Conectando a {host} vía SFTP...")
        ssh.connect(host, port=puerto, username=usuario, password=clave, timeout=10)

        # 4. Abrimos una sesión SFTP sobre el túnel SSH
        sftp = ssh.open_sftp()
        
        # 5. Definimos la ruta de destino en el servidor
        # Esta carpeta la creamos previamente con: sudo mkdir -p /var/sftp/uploads
        ruta_remota = f"/var/sftp/uploads/{nombre_destino}"
        
        # 6. Realizamos la transferencia (Cargar archivo)
        sftp.put(ruta_local, ruta_remota)
        
        # 7. Cerramos sesión
        sftp.close()
        ssh.close()
        print("Transferencia SFTP completada con éxito.")
        return True

    except Exception as e:
        # Si algo falla (ej. servicio SSH apagado), capturamos el error
        print(f"Error crítico en la conexión SFTP: {e}")
        if ssh:
            ssh.close()
        return False