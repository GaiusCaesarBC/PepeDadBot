"""
╔══════════════════════════════════════════════════════════════╗
║           WATCHER NODE — ARCHIVE INTERFACE v1.0              ║
║           $PEPEDAD ARG Telegram Bot                          ║
║           Status: ACTIVE — Signal monitoring enabled         ║
╚══════════════════════════════════════════════════════════════╝

A Telegram bot for the $PEPEDAD Solana ARG investigation.
Built with python-telegram-bot.

"""

import os
import random
import base64
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────
# ENV SETUP
# ─────────────────────────────────────────────

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found. Add it to your .env file.")

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════
#   LORE CONFIGURATION — EDIT THIS SECTION
#   All story content lives here. Change freely.
# ══════════════════════════════════════════════

# ─── CLUES ────────────────────────────────────
# Returned randomly by /clue
CLUES = [
    "04:13:07",
    "IT FOLLOWED HIM BACK.",
    "You were noticed before you started looking.",
    "No upload origin found.",
    "The archive did not create this file.",
    "He returned unchanged. The timestamps did not.",
    "Cross-reference suppressed — reason: FOREIGN.",
    "Signal detected at origin point. Origin point should not exist.",
    "Three entries. Three deletions. One remains.",
    "The last frame of the recording was not recorded.",
    "Pattern match: 94.7% — source: unknown.",
    "This transmission arrived before it was sent.",
    "His shadow arrives 0.4 seconds before he does.",
    "The milk was purchased. The receipt is dated tomorrow.",
    "Watcher event logged. You are not the first to read this.",
    "REDACTED — authorization tier insufficient.",
    "Two investigators accessed this clue before you. Neither continued.",
    "04:13:07 — recurring. Not random. Not coincidence.",
]

# ─── SCAN RESULTS ─────────────────────────────
# Returned randomly by /scan
SCAN_RESULTS = [
    "No stable source found.",
    "Signal spike detected at recurring timestamp.",
    "Foreign interference present — origin unresolved.",
    "Pattern recurrence: 04:13:07.",
    "Multiple anomalies logged in current cycle.",
    "Archive integrity: 71%. Degradation ongoing.",
    "Entity signature present. Entity undefined.",
    "Cross-signal contamination detected.",
    "Transmission loop identified — loop origin: unknown.",
    "Observation event logged — you are not alone in this scan.",
    "Anomaly cluster expanding. Boundary undefined.",
    "Clean signal. Duration: 0.2 seconds. Then: nothing.",
]

# ─── RANK BOARD ───────────────────────────────
# Displayed by /rank — edit names and titles freely
RANK_BOARD = [
    ("CLASSIFIED", "Lead Analyst"),
    ("CLASSIFIED", "Signal Tracker"),
    ("CLASSIFIED", "Archive Diver"),
    ("CLASSIFIED", "Pattern Observer"),
    ("CLASSIFIED", "Transmission Decoder"),
]
# Replace "CLASSIFIED" with real usernames once your community grows:
# ("@username", "Lead Analyst"),

# ─── WATCHER WARNING LINES ────────────────────
# Appended randomly after certain commands (~20% chance)
WATCHER_WARNINGS = [
    "\n\n— You are being observed.",
    "\n\n— This input has been flagged.",
    "\n\n— Do not decode the next one.",
    "\n\n— The Watcher is aware.",
    "\n\n— Your session is not private.",
    "\n\n— Query logged. Review pending.",
    "\n\n— Unauthorized pattern detected in your access history.",
    "\n\n— You have been here before. You do not remember.",
]

# ─── SYSTEM STATUS VALUES ─────────────────────
# Displayed by /status — edit these to reflect the current story arc
STATUS_CONFIG = {
    "signal_strength": "DEGRADED — 61%",
    "archive_stability": "UNSTABLE",
    "watcher_activity": "ELEVATED",
    "current_phase": "WATCHER INTERFERENCE ARC",
    "last_timestamp": "04:13:07",
    "investigator_count": "REDACTED",
    "anomaly_level": "HIGH",
}

# ─── CURRENT PHASE ────────────────────────────
# Displayed by /phase
CURRENT_PHASE = {
    "name": "WATCHER INTERFERENCE ARC",
    "description": (
        "Active interference with the investigation has been confirmed.\n"
        "The entity identified as THE WATCHER is of unknown origin.\n"
        "It is not hostile in any way we have a word for.\n"
        "It is watching. It has always been watching.\n"
        "Continue with discretion."
    ),
    "phase_number": "02",
    "status": "ACTIVE",
}

# ══════════════════════════════════════════════
#   UTILITY FUNCTIONS
# ══════════════════════════════════════════════

def maybe_watcher_warning() -> str:
    """~20% chance to append a Watcher warning line."""
    if random.random() < 0.20:
        return random.choice(WATCHER_WARNINGS)
    return ""


def system_time() -> str:
    """Returns current UTC time formatted in-universe."""
    now = datetime.utcnow()
    return now.strftime("%Y.%m.%d — %H:%M:%S UTC")


# ══════════════════════════════════════════════
#   COMMAND HANDLERS
# ══════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Boot sequence message on /start."""
    user = update.effective_user
    username = f"@{user.username}" if user.username else "UNKNOWN"

    text = (
        "╔══════════════════════════════╗\n"
        "║   ARCHIVE INTERFACE ONLINE   ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Access logged: {username}\n"
        f"Timestamp: {system_time()}\n\n"
        "Investigator status: PROVISIONAL\n"
        "Clearance level: TIER 0\n\n"
        "You are entering an active investigation.\n"
        "Subject: PEPEDAD — returned, unchanged.\n"
        "Threat: THE WATCHER — present.\n\n"
        "Proceed with caution.\n"
        "Type /help to access command index."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """In-universe help / command index."""
    text = (
        "╔══════════════════════════════╗\n"
        "║   COMMAND INDEX — RESTRICTED ║\n"
        "╚══════════════════════════════╝\n\n"
        "/start      — Initialize session\n"
        "/status     — System status report\n"
        "/clue       — Retrieve archive fragment\n"
        "/decode     — Decode transmission [input]\n"
        "/scan       — Run anomaly scan\n"
        "/rank       — Personnel board\n"
        "/report     — Submit investigator report\n"
        "/phase      — Current arc status\n"
        "/timestamp  — Recurring signal reference\n\n"
        "Additional commands exist.\n"
        "They are not listed here."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Live-feeling system status report."""
    s = STATUS_CONFIG
    text = (
        "╔══════════════════════════════╗\n"
        "║     SYSTEM STATUS REPORT     ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Signal Strength      : {s['signal_strength']}\n"
        f"Archive Stability    : {s['archive_stability']}\n"
        f"Watcher Activity     : {s['watcher_activity']}\n"
        f"Anomaly Level        : {s['anomaly_level']}\n"
        f"Current Phase        : {s['current_phase']}\n"
        f"Active Investigators : {s['investigator_count']}\n"
        f"Last Known Timestamp : {s['last_timestamp']}\n\n"
        f"Report generated: {system_time()}"
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def clue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns a random clue fragment from the archive."""
    fragment = random.choice(CLUES)
    text = (
        "╔══════════════════════════════╗\n"
        "║    ARCHIVE FRAGMENT LOCATED  ║\n"
        "╚══════════════════════════════╝\n\n"
        f"{fragment}\n\n"
        "— Fragment integrity: unverified.\n"
        "— Source: UNKNOWN."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Decodes a Base64 string passed after /decode."""
    if not context.args:
        await update.message.reply_text(
            "DECODE ERROR\n\n"
            "No input received.\n"
            "Usage: /decode [base64 string]"
        )
        return

    raw_input = " ".join(context.args).strip()

    try:
        # Attempt Base64 decode
        decoded_bytes = base64.b64decode(raw_input)
        decoded_text = decoded_bytes.decode("utf-8")

        text = (
            "╔══════════════════════════════╗\n"
            "║      DECODE SUCCESSFUL       ║\n"
            "╚══════════════════════════════╝\n\n"
            f"{decoded_text}\n\n"
            "— Transmission recovered.\n"
            "— Origin: unresolvable."
            + maybe_watcher_warning()
        )
    except Exception:
        text = (
            "╔══════════════════════════════╗\n"
            "║        DECODE FAILED         ║\n"
            "╚══════════════════════════════╝\n\n"
            "Input corrupted or unreadable.\n"
            "Fragment may be intentionally damaged.\n\n"
            "— Or you were not meant to read it."
            + maybe_watcher_warning()
        )

    await update.message.reply_text(text)


async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns the investigator rank board."""
    board_lines = ""
    for i, (name, title) in enumerate(RANK_BOARD, start=1):
        board_lines += f"  {i}. {name:<18} — {title}\n"

    text = (
        "╔══════════════════════════════╗\n"
        "║   INVESTIGATOR PERSONNEL     ║\n"
        "║   BOARD — RESTRICTED ACCESS  ║\n"
        "╚══════════════════════════════╝\n\n"
        + board_lines
        + "\n— Records sealed.\n"
        "— Some entries are not visible at your clearance level."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns a random anomaly scan result."""
    result = random.choice(SCAN_RESULTS)
    text = (
        "╔══════════════════════════════╗\n"
        "║      ANOMALY SCAN ACTIVE     ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Scanning...\n\n"
        f"RESULT: {result}\n\n"
        f"Scan completed: {system_time()}"
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Accepts and acknowledges an investigator report."""
    user = update.effective_user
    username = f"@{user.username}" if user.username else "UNKNOWN"

    if context.args:
        submission = " ".join(context.args)
        logger.info(f"REPORT from {username}: {submission}")
        content_line = f'Received: "{submission[:200]}"\n\n'
    else:
        content_line = "No content body detected.\nSubmit theory after command.\n\n"

    text = (
        "╔══════════════════════════════╗\n"
        "║       REPORT LOGGED          ║\n"
        "╚══════════════════════════════╝\n\n"
        + content_line
        + f"Filed by: {username}\n"
        f"Timestamp: {system_time()}\n\n"
        "Archive review pending.\n"
        "Investigators are advised: not all reports are read by humans."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns the current story arc / phase status."""
    p = CURRENT_PHASE
    text = (
        "╔══════════════════════════════╗\n"
        "║     CURRENT PHASE STATUS     ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Phase {p['phase_number']}: {p['name']}\n"
        f"Status: {p['status']}\n\n"
        f"{p['description']}"
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def timestamp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns the recurring signal timestamp with context."""
    text = (
        "╔══════════════════════════════╗\n"
        "║     RECURRING SIGNAL REF     ║\n"
        "╚══════════════════════════════╝\n\n"
        "04:13:07\n\n"
        "This timestamp appears across 14 separate recovered fragments.\n"
        "It does not correspond to any verified event.\n"
        "It predates the archive.\n\n"
        "Its origin has not been located.\n"
        "Its repetition is not accidental.\n\n"
        "Do not search for it."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles unknown commands — keeps it in-universe."""
    text = (
        "UNRECOGNIZED INPUT\n\n"
        "Command not found in this interface.\n"
        "If you believe this command exists — it may require higher clearance.\n\n"
        "— Input flagged."
        + maybe_watcher_warning()
    )
    await update.message.reply_text(text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler."""
    logger.error(f"Error: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "SYSTEM ERROR\n\n"
            "An unexpected fault occurred.\n"
            "Archive integrity may be compromised.\n\n"
            "— Error logged. Session continuing."
        )


# ══════════════════════════════════════════════
#   MAIN — BOT INITIALIZATION
# ══════════════════════════════════════════════

def main() -> None:
    """Start the Watcher Node."""
    logger.info("WATCHER NODE — Initializing...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("clue", clue))
    app.add_handler(CommandHandler("decode", decode))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("phase", phase))
    app.add_handler(CommandHandler("timestamp", timestamp))

    # Catch-all for unrecognized commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Global error handler
    app.add_error_handler(error_handler)

    logger.info("WATCHER NODE — Online. Polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
