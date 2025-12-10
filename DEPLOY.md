# Guía de Despliegue en Render con Neon Database

Esta guía te ayudará a desplegar el proyecto Django en Render usando Neon como base de datos PostgreSQL.

## 1. Preparación del Repositorio

El proyecto ya está configurado con:
- `procfile`: Para indicar a Render cómo arrancar la app.
- `build.sh`: Script para instalar dependencias, recoger estáticos y migrar la BD.
- `requirements.txt`: Lista de dependencias (incluye `gunicorn`, `dj-database-url`, `psycopg-binary`).
- `settings.py`: Configurado para leer variables de entorno.

### Subir a GitHub
Si aún no has subido el código:
```bash
git remote add origin https://github.com/cristian08leal/FastFood.git
git branch -M main
git push -u origin main
```
*(Asegúrate de haber creado el repositorio `FastFood` en tu cuenta de GitHub antes de hacer push).*

## 2. Configuración Base de Datos (Neon)

1. Ve a [Neon Console](https://console.neon.tech/) y crea una cuenta/login.
2. Crea un **Nuevo Proyecto**.
3. Una vez creado, busca el **Connection String** en el Dashboard.
   - Selecciona "Direct Connection" o "Pooled Connection" (Direct suele estar bien para Django persistente, pero Pooled es mejor para escalar).
   - Copia la URL que se ve así: `postgres://usuario:password@ep-xyz.aws.neon.tech/neondb?sslmode=require`

## 3. Configuración en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/).
2. Haz clic en **New +** -> **Web Service**.
3. Conecta tu repositorio de GitHub (`cristian08leal/FastFood`).
4. Configura los siguientes campos:

| Campo | Valor |
|-------|-------|
| Name | `fastfood-backend` (o el que gustes) |
| Region | Oregon (US West) o la más cercana y barata |
| Branch | `main` |
| Runtime | **Python 3** |
| Build Command | `./build.sh` |
| Start Command | `gunicorn mi_proyecto.wsgi:application` |
| Instance Type | Free (para pruebas) o Starter |

5. **IMPORTANTE**: Ve a la sección **Environment Variables** y añade las siguientes variables:

| Variable | Valor / Descripción |
|----------|---------------------|
| `DATABASE_URL` | Pega aquí la Connection String de Neon que copiaste en el paso 2. |
| `SECRET_KEY` | Genera una clave segura (puedes usar un generador online). |
| `DEBUG` | `False` (Para producción). |
| `PYTHON_VERSION` | `3.11.5` (Opcional, para asegurar versión). |
| `CSRF_TRUSTED_ORIGINS` | El dominio que Render te asigne, e.g., `https://fastfood-backend.onrender.com`. (Puedes añadirlo después del primer despliegue fallido si es necesario, o usar `https://*.onrender.com`). |

### Configuración para Email (Doble Verificación)

Para que funcione la doble verificación (2FA), necesitas un servidor SMTP. Si usas Gmail:

1. Ve a tu cuenta de Google -> Seguridad -> Verificación en 2 pasos -> **Contraseñas de aplicaciones**.
2. Genera una contraseña para "Correo" / "Render".
3. Añade estas variables en Render:

| Variable | Valor |
|----------|-------|
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `tu_correo@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `la_contraseña_de_aplicacion_generada` |

## 4. Despliegue

Haz clic en **Create Web Service**. Render empezará a construir el proyecto.
Puedes ver los logs en tiempo real. 

Si el script `./build.sh` falla por permisos, Render suele manejarlo bien, pero asegúrate de que el archivo tenga permisos de ejecución en git (`git update-index --chmod=+x build.sh`).

## 5. Verificar Despliegue

Una vez que Render diga "Live", visita la URL proporcionada.
Prueba el registro y login. Deberías recibir un correo con el código de verificación (si configuraste las variables de email correctamente).

## Solución de Problemas Comunes

- **Error de base de datos**: Verifica que `DATABASE_URL` sea correcta y empiece por `postgres://`.
- **Error de estáticos**: Si los estilos no cargan, verifica que `build.sh` haya ejecutado `collectstatic` correctamente.
- **Error 500**: Pon `DEBUG=True` temporalmente en las variables de entorno para ver el error detallado, pero **nunca lo dejes en True en producción**.
