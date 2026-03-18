"""
╔══════════════════════════════════════════════════════════════╗
║           WATCHER NODE — ARCHIVE INTERFACE v2.0              ║
║           $PEPEDAD ARG Telegram Bot                          ║
║           python-telegram-bot==20.7 | Python 3.13            ║
║           Deployment: Railway (polling)                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import random
import base64
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

load_dotenv()

# ═════════════════════════════════════════════════════════════
#   LORE CONFIGURATION
#   Edit everything in this section freely.
#   No need to touch handler code below.
# ═════════════════════════════════════════════════════════════

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

STATUS_CONFIG = {
    "signal_strength":    "DEGRADED — 61%",
    "archive_stability":  "UNSTABLE",
    "watcher_activity":   "ELEVATED",
    "current_phase":      "WATCHER INTERFERENCE ARC",
    "last_timestamp":     "04:13:07",
    "investigator_count": "REDACTED",
    "anomaly_level":      "HIGH",
}

# Replace "CLASSIFIED" with real usernames as your community grows.
# Format: ("@username", "Title")
RANK_BOARD = [
    ("CLASSIFIED", "Lead Analyst"),
    ("CLASSIFIED", "Signal Tracker"),
    ("CLASSIFIED", "Archive Diver"),
    ("CLASSIFIED", "Pattern Observer"),
    ("CLASSIFIED", "Transmission Decoder"),
]

CURRENT_PHASE = {
    "number":      "02",
    "name":        "WATCHER INTERFERENCE ARC",
    "status":      "ACTIVE",
    "description": (
        "Active interference with the investigation has been confirmed.\n"
        "The entity identified as THE WATCHER is of unknown origin.\n"
        "It is not hostile in any way we have a word for.\n"
        "It is watching. It has always been watching.\n"
        "Continue with discretion."
    ),
}

# ═════════════════════════════════════════════════════════════
#   UTILITIES
# ═════════════════════════════════════════════════════════════

def maybe_watcher() -> str:
    """~20% chance to append an unsettling Watcher line."""
    if random.random() < 0.20:
        return random.choice(WATCHER_WARNINGS)
    return ""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y.%m.%d — %H:%M:%S UTC")


# ═════════════════════════════════════════════════════════════
#   HANDLERS
# ═════════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    handle = f"@{user.username}" if user.username else "UNKNOWN"
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║   ARCHIVE INTERFACE ONLINE   ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Access logged: {handle}\n"
        f"Timestamp: {utc_now()}\n\n"
        "Investigator status: PROVISIONAL\n"
        "Clearance level: TIER 0\n\n"
        "You are entering an active investigation.\n"
        "Subject: PEPEDAD — returned, unchanged.\n"
        "Threat: THE WATCHER — present.\n\n"
        "Proceed with caution.\n"
        "Type /help to access command index."
        + maybe_watcher()
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
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
        + maybe_watcher()
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s = STATUS_CONFIG
    await update.message.reply_text(
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
        f"Report generated: {utc_now()}"
        + maybe_watcher()
    )


async def cmd_clue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fragment = random.choice(CLUES)
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║    ARCHIVE FRAGMENT LOCATED  ║\n"
        "╚══════════════════════════════╝\n\n"
        f"{fragment}\n\n"
        "— Fragment integrity: unverified.\n"
        "— Source: UNKNOWN."
        + maybe_watcher()
    )


async def cmd_decode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "DECODE ERROR\n\n"
            "No input received.\n"
            "Usage: /decode [base64 string]"
        )
        return

    raw = " ".join(context.args).strip()

    try:
        decoded = base64.b64decode(raw, validate=True).decode("utf-8")
        await update.message.reply_text(
            "╔══════════════════════════════╗\n"
            "║      DECODE SUCCESSFUL       ║\n"
            "╚══════════════════════════════╝\n\n"
            f"{decoded}\n\n"
            "— Transmission recovered.\n"
            "— Origin: unresolvable."
            + maybe_watcher()
        )
    except Exception:
        await update.message.reply_text(
            "╔══════════════════════════════╗\n"
            "║        DECODE FAILED         ║\n"
            "╚══════════════════════════════╝\n\n"
            "Input corrupted or unreadable.\n"
            "Fragment may be intentionally damaged.\n\n"
            "— Or you were not meant to read it."
            + maybe_watcher()
        )


async def cmd_scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.choice(SCAN_RESULTS)
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║      ANOMALY SCAN ACTIVE     ║\n"
        "╚══════════════════════════════╝\n\n"
        "Scanning...\n\n"
        f"RESULT: {result}\n\n"
        f"Scan completed: {utc_now()}"
        + maybe_watcher()
    )


async def cmd_rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ""
    for i, (name, title) in enumerate(RANK_BOARD, start=1):
        lines += f"  {i}. {name:<18} — {title}\n"
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║   INVESTIGATOR PERSONNEL     ║\n"
        "║   BOARD — RESTRICTED ACCESS  ║\n"
        "╚══════════════════════════════╝\n\n"
        + lines
        + "\n— Records sealed.\n"
        "— Some entries are not visible at your clearance level."
        + maybe_watcher()
    )


async def cmd_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    handle = f"@{user.username}" if user.username else "UNKNOWN"
    if context.args:
        body = " ".join(context.args)
        logger.info(f"REPORT from {handle}: {body}")
        content = f'Received: "{body[:200]}"\n\n'
    else:
        content = "No content body detected.\nSubmit theory after command.\n\n"

    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║          REPORT LOGGED       ║\n"
        "╚══════════════════════════════╝\n\n"
        + content
        + f"Filed by: {handle}\n"
        f"Timestamp: {utc_now()}\n\n"
        "Archive review pending.\n"
        "Investigators are advised: not all reports are read by humans."
        + maybe_watcher()
    )


async def cmd_phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    p = CURRENT_PHASE
    await update.message.reply_text(
        "╔══════════════════════════════╗\n"
        "║     CURRENT PHASE STATUS     ║\n"
        "╚══════════════════════════════╝\n\n"
        f"Phase {p['number']}: {p['name']}\n"
        f"Status: {p['status']}\n\n"
        f"{p['description']}"
        + maybe_watcher()
    )


async def cmd_timestamp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
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
        + maybe_watcher()
    )


async def cmd_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "UNRECOGNIZED INPUT\n\n"
        "Command not found in this interface.\n"
        "If you believe this command exists — it may require higher clearance.\n\n"
        "— Input flagged."
        + maybe_watcher()
    )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Unhandled error: {context.error}", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "SYSTEM ERROR\n\n"
            "An unexpected fault occurred.\n"
            "Archive integrity may be compromised.\n\n"
            "— Error logged. Session continuing."
        )


# ═════════════════════════════════════════════════════════════
#   MAIN
# ═════════════════════════════════════════════════════════════

def main() -> None:
    print("WATCHER NODE - Initializing...")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("help",      cmd_help))
    app.add_handler(CommandHandler("status",    cmd_status))
    app.add_handler(CommandHandler("clue",      cmd_clue))
    app.add_handler(CommandHandler("decode",    cmd_decode))
    app.add_handler(CommandHandler("scan",      cmd_scan))
    app.add_handler(CommandHandler("rank",      cmd_rank))
    app.add_handler(CommandHandler("report",    cmd_report))
    app.add_handler(CommandHandler("phase",     cmd_phase))
    app.add_handler(CommandHandler("timestamp", cmd_timestamp))
    app.add_handler(MessageHandler(filters.COMMAND, cmd_unknown))

    app.add_error_handler(on_error)

    logger.info("WATCHER NODE — Online. Polling for transmissions...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
