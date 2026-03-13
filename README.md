# Tu Caserito — Auth Service

Servicio encargado de la autenticación de usuarios mediante Google y manejo de tokens JWT.

## Security Policy
**Atención a nivel de Arquitectura Security (Hardening)**:
- **No commitear secretos**: Está estrictamente prohibido subir el archivo `.env` o cualquier secreto/llave al control de versiones. Usa siempre `.env.example` como referencia.
- **X-Admin-Key**: Cualquier llave referida como `X-Admin-Key` o similar es una solución **temporal** (Deuda Técnica). Se debe limitar su exposición estrictamente al backend (Service-to-Service) y jamás debe ser expuesta o enviada desde el navegador del usuario original.
