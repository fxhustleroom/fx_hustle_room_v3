# FX Hustle Room

Production-ready Telegram Forex Signals Ecosystem built with aiogram 3, PostgreSQL, FastAPI webhook support, and Streamlit admin panel.

## Features
- onboarding bot with 10-language selection
- rules & terms acceptance
- trading account + KYC + funding onboarding
- deposit proof upload and admin approval
- risk confirmation flow
- first signal + Telegram trading video delivery
- first trade proof upload and admin approval
- premium access gating
- MT5 / TradingView style webhook endpoint
- Streamlit admin dashboard
- PostgreSQL persistence with SQLAlchemy
- Docker-ready structure

## Folder Structure
```text
app/
  handlers/
    admin.py
    onboarding.py
    signals.py
    start.py
  config.py
  db.py
  keyboards.py
  languages.py
  models.py
  states.py
  texts.py
main.py
admin_panel/
  streamlit_app.py
requirements.txt
.env.example
```

## Setup
1. Copy `.env.example` to `.env`
2. Fill in the values
3. Create the PostgreSQL database and user, or run Docker Compose
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the bot + webhook API:
   ```bash
   python main.py
   ```
6. Run the Streamlit admin panel in another terminal:
   ```bash
   streamlit run admin_panel/streamlit_app.py
   ```

## Database quick start
```sql
CREATE USER fxuser WITH PASSWORD 'fxpass';
CREATE DATABASE fx_hustle_room;
ALTER DATABASE fx_hustle_room OWNER TO fxuser;
```

## Docker quick start
```bash
docker compose up --build
```

## Admin bot commands
- `/start`
- `/admin_stats`
- `/set_trading_video` then upload a Telegram video
- `/set_first_signal` then send the signal text to save as default

## Webhook Endpoint
`POST /webhook/signal`

Example payload:
```json
{
  "pair": "XAUUSD",
  "direction": "BUY",
  "entry": 2320.50,
  "sl": 2315.00,
  "tp1": 2325.00,
  "tp2": 2330.00,
  "risk_percentage": 1.0,
  "chart_image_url": null
}
```

PowerShell test:
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/webhook/signal -ContentType "application/json" -Body '{"pair":"XAUUSD","direction":"BUY","entry":2320.5,"sl":2315.0,"tp1":2325.0,"tp2":2330.0,"risk_percentage":1.0}'
```

## Example signal format
```text
XAUUSD BUY, Entry: 2320.50, Stop Loss: 2315.00, Take Profit 1: 2325.00, Take Profit 2: 2330.00, Risk: 1.0%

Entry: 2320.50
Stop Loss: 2315.00
Take Profit 1: 2325.00
Take Profit 2: 2330.00
Risk: 1.0%
```

## Trading video
Use `/set_trading_video` from an admin chat, then upload the actual Telegram video. The bot stores the `file_id` and reuses it for every qualified user.

## Security note
If you pasted a real Telegram bot token anywhere public, rotate it in BotFather before deploying.
