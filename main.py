import subprocess
import re
import pandas as pd

# Lista de servidores en diferentes partes del mundo
servers = {
    "ETB (Bogotá)": "www.etb.com",
    "Claro (Colombia)": "www.claro.com.co",
    "Movistar (Colombia)": "www.movistar.com.co",
    "Tigo (Colombia)": "www.tigo.com.co",
    "AWS (Virginia, EE.UU.)": "ec2.us-east-1.amazonaws.com",
    "Google (São Paulo, Brasil)": "google.com.br",
    "AWS (São Paulo, Brasil)": "ec2.sa-east-1.amazonaws.com",
    "BBC (Reino Unido)": "www.bbc.co.uk",
    "AWS (Fráncfort, Alemania)": "ec2.eu-central-1.amazonaws.com",
}

# Función para hacer ping y obtener la latencia promedio
def ping_server(server_name, server_ip):
    try:
        print(f"Haciendo ping a {server_name} ({server_ip})...")
        result = subprocess.run(
            ["ping", "-c", "4", server_ip], capture_output=True, text=True
        )
        if result.returncode == 0:
            # Buscar la línea que contiene la latencia promedio (en sistemas Linux)
            match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)', result.stdout)
            if match:
                avg_latency = float(match.group(2))  # Extraer el valor promedio
                print(f"Latencia promedio a {server_name}: {avg_latency} ms")
                return avg_latency
            else:
                print(f"No se pudo calcular la latencia para {server_name}")
                return None
        else:
            print(f"Error al hacer ping a {server_name}")
            return None
    except Exception as e:
        print(f"Excepción al hacer ping a {server_name}: {e}")
        return None


# Diccionario para almacenar resultados
latency_results = {}

# Hacer ping a cada servidor y almacenar la latencia
for server_name, server_ip in servers.items():
    latency = ping_server(server_name, server_ip)
    if latency is not None:
        latency_results[server_name] = latency

# Crear un DataFrame para organizar los resultados
df = pd.DataFrame(list(latency_results.items()), columns=["Servidor", "Latencia (ms)"])

# Ordenar por latencia de menor a mayor (mejor a peor)
df = df.sort_values(by="Latencia (ms)")

# Mostrar los resultados en un cuadro final
print("\nResultados de latencia (mejor a peor):\n")
print(df)
