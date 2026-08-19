# Formulario de newsletter

## Dónde está

En dos lugares, en los tres idiomas:

| Ubicación | Páginas |
|---|---|
| Footer, debajo del bloque de redes sociales | las 54 |
| Sección propia, entre los testimonios de clientes y el CTA comercial | `index.html` y `cfo.html` en es / en / pt (6) |

Campos: **nombre y apellido**, **email**, **empresa** y **país** (desplegable con 21 países más «Otro»). Los cuatro son obligatorios.

## Falta definir el destino de los datos

**Hoy las suscripciones no llegan a ningún lado.** Mientras `endpoint` esté vacío, el formulario valida, muestra la confirmación y guarda el alta en `localStorage` bajo la clave `rb-nl-pending`, para no perderla. En la consola queda un aviso en cada envío.

Para conectarlo, editar la configuración al principio del bloque `<script id="rb-nl-js">`:

```js
var CFG = { endpoint: '', enabled: true };
```

- **`endpoint`** — URL que recibe un `POST` con `Content-Type: application/json`. Sirve cualquier cosa que acepte un POST: un form de Clientify, un webhook de Make o Zapier, una función de Vercel, un endpoint propio. El cuerpo es:

  ```json
  {
    "name": "Frani Gómez",
    "email": "frani@empresa.com",
    "company": "Rocketbot",
    "country": "Chile",
    "lang": "es",
    "page": "/index.html",
    "sentAt": "2026-08-19T15:33:59.406Z"
  }
  ```

  El formulario considera exitoso cualquier `response.ok`; si falla, muestra el mensaje de error y no limpia los campos, así el visitante puede reintentar sin volver a escribir todo.

- **`enabled`** — poner en `false` oculta los dos bloques sin tocar el HTML. Útil si se prefiere no exponer el formulario hasta tener el destino resuelto.

Cambiar cualquiera de los dos valores en `build_newsletter.py` y volver a correrlo actualiza las 54 páginas de una vez.

## Cómo se edita

**No editar el HTML a mano**: el bloque está duplicado en 54 archivos. Todo (textos, campos, países, estilos y lógica) vive en `build_newsletter.py`.

```bash
python build_newsletter.py            # simulación: dice qué tocaría
python build_newsletter.py --apply    # escribe
```

Es idempotente y re-ejecutable: si el bloque ya está, no lo duplica; si el CSS cambió, lo reemplaza en su lugar.

## Notas

- Los textos de los tres idiomas están en el diccionario `T` al principio del script; los países, en `COUNTRIES`.
- El bloque de la sección se inserta antes de `<section class="rb-cta-band">`. Para llevarlo a más páginas, agregar el nombre del archivo al conjunto `WITH_SECTION` en `main()`.
- Contraste verificado en tema claro y oscuro: bordes de campo 3.5:1 y texto por encima de 15:1, sobre el mínimo de WCAG.
- El enlace a las políticas de privacidad apunta a la versión del idioma de cada página.
