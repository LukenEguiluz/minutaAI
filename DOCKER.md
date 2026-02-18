# MinutaAI con Docker

Guía para ejecutar MinutaAI en Docker, accesible desde VPN o mediante un dominio.

## Ejecutar

```bash
# Construir imagen y levantar
docker compose up -d

# Ver estado
docker compose ps

# Ver logs en tiempo real
docker compose logs -f minutaai

# Detener
docker compose down
```

La aplicación queda expuesta en el puerto **5000** y escucha en `0.0.0.0`, así que es accesible desde:

- `http://localhost:5000` (en la misma máquina)
- `http://<IP-de-tu-PC>:5000` (en tu red local)
- `http://<IP-o-hostname>:5000` (desde tu VPN, si tu PC tiene IP accesible vía VPN)

## Acceso desde VPN

1. Asegúrate de que Docker publica el puerto: `ports: "5000:5000"` (ya está en `docker-compose.yml`).
2. Conecta tu VPN a la red donde está tu PC.
3. Usa la IP local de tu PC o su hostname en la VPN: `http://<IP>:5000`.
4. En el firewall de Windows, permite tráfico entrante en el puerto 5000 (TCP).

## Puentear a un dominio

Para acceder con un dominio (p.ej. `minuta.midominio.com`):

### Opción 1: Cloudflare Tunnel (sin abrir puertos)

1. Crea una cuenta en [Cloudflare Zero Trust](https://one.cloudflare.com/).
2. Instala `cloudflared` en tu PC.
3. Configura un túnel que enruta tu dominio al `localhost:5000`.

### Opción 2: Nginx (reverse proxy) + DNS/port forwarding

1. Configura que tu dominio apunte a la IP pública de tu router.
2. En el router, redirige el puerto 80/443 a tu PC.
3. Instala nginx (en Docker o nativo) y apunta al contenedor:

```yaml
# Ejemplo nginx proxy (si añades nginx a docker-compose)
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/conf.d/default.conf
  depends_on:
    - minutaai
```

```nginx
# nginx.conf
server {
    listen 80;
    server_name minuta.tudominio.com;
    location / {
        proxy_pass http://minutaai:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Opción 3: Tailscale

1. Instala [Tailscale](https://tailscale.com/) en tu PC y en los dispositivos que quieras que accedan.
2. Activa Tailscale Funnel o usa la IP de Tailscale de tu PC: `http://100.x.x.x:5000`.

## Variables de entorno opcionales

Puedes definir en `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - WHISPER_MODEL=base   # tiny, base, small, medium, large
```

Para cambiar el modelo Whisper, ajusta `config.py` o expón la variable `WHISPER_MODEL` si lo implementas en la app.

## Volúmenes

Los archivos subidos se guardan en el volumen `minutaai_uploads`. Para respaldar o migrar:

```bash
# Ubicación del volumen
docker volume inspect minutaai_minutaai_uploads
```

## Primera ejecución

La primera vez que arranque el contenedor, Whisper descargará el modelo (p.ej. `base`, ~140MB). Puede tardar unos minutos según tu conexión.
