# StudentOverflow (Flask + Supabase)

Portal de preguntas y respuestas inspirado en StackOverflow.

## Requisitos
- Python 3.10+
- Cuenta y proyecto en Supabase

## Configuración
1. Crea las tablas ejecutando el SQL de `supabase_schema.sql` en el editor SQL de Supabase.
2. Copia `.env.example` a `.env` y completa:
   - `FLASK_SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY` (server-side)
   - `SUPABASE_ANON_KEY` (para auth)
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la app:
   ```bash
   python run.py
   ```
