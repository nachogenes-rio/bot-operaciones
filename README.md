# Bot de Operaciones - WhatsApp 🍔

Bot de WhatsApp que responde preguntas sobre el tablero de operaciones de la planta en lenguaje natural.

## Estructura del proyecto

```
bot/
├── app.py                  # Servidor principal
├── test_local.py           # Prueba sin WhatsApp
├── requirements.txt
├── data/
│   └── operaciones.xlsx    # ← COPIAR ACA EL EXCEL
└── utils/
    ├── excel_reader.py     # Lee el Excel
    └── claude_handler.py   # Conecta con Claude
```

## Paso 1: Preparar el Excel

Copiar el archivo `Tablero_Resumido.xlsx` dentro de la carpeta `data/` y renombrarlo a `operaciones.xlsx`.

## Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

## Paso 3: Variables de entorno

Crear un archivo `.env` con:

```
ANTHROPIC_API_KEY=tu_clave_aqui
```

## Paso 4: Probar localmente

```bash
python test_local.py
```

Ejemplos de preguntas:
- "¿Cuánto produjeron hoy?"
- "¿Cuántos camiones balancín salieron?"
- "¿Cuál fue la eficiencia del turno tarde?"
- "¿Cuánto produjeron en enero 2025?"
- "¿Qué temas de calidad están pendientes?"
- "¿Hubo devoluciones este mes?"
- "Comparame la eficiencia de los últimos 7 días"

## Paso 5: Desplegar en Railway

1. Crear cuenta en [Railway](https://railway.app)
2. Subir este proyecto a GitHub
3. En Railway: New Project → Deploy from GitHub
4. Agregar la variable `ANTHROPIC_API_KEY` en Settings → Variables
5. Railway te da una URL pública (ej: `https://bot-xxx.railway.app`)

## Paso 6: Conectar con Twilio (WhatsApp)

1. Crear cuenta en [Twilio](https://twilio.com)
2. Ir a Messaging → Try it out → Send a WhatsApp message
3. Configurar el webhook: `https://tu-url-railway.app/webhook`
4. Método: POST

## Actualizar el Excel

Para actualizar los datos, reemplazá el archivo `data/operaciones.xlsx` con la versión nueva.
En Railway podés hacerlo vía la CLI o conectando un volumen persistente.

## Datos que responde el bot

| Categoría | Datos |
|-----------|-------|
| Producción | KG por día, TM, TT |
| Eficiencia | % total, por turno |
| Calidad | Merma %, Decomiso % |
| Logística | Semis, balancines, chasis, camionetas por zona |
| Mensual | Producción real vs objetivo, histórico |
| Temas | Plan de acción por sector |
| Devoluciones | Por cliente, producto, motivo |
| Recortes | Productos no producidos y razón |
