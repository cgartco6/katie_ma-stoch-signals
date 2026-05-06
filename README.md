# Katie MA + Stochastic Signals Bot

Replicates Katie's strategy from: https://youtu.be/pojqs15lHg8

**Features:**
- 1-minute Heikin Ashi style logic
- SMA 4 (Green), SMA 50 (Red), SMA 200 (White)
- Stochastic 5,1,1
- **Pre-Signal** (early warning) + **Confirmed Signal**
- Telegram alerts
- No risk management (as requested)

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` → `.env` and fill Telegram details
3. `python main.py`

**Warning**: High risk strategy. Use on demo only. Not financial advice.
