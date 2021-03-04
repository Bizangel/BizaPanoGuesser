from pyngrok import ngrok
import subprocess

if __name__ == '__main__':
    http_tunnel = ngrok.connect(6789, bind_tls=True)
    tunnels = ngrok.get_tunnels()

    subprocess.run(["python", "mainServer.py", tunnels[0].public_url])
