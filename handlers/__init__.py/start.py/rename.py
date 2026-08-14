from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import ADMIN_IDS


def register(app, db):

    @app.on_message(
        filters.command("start")
    )
    async def start_handler(
        client,
        message,
    ):

        buttons = [
            [
                InlineKeyboardButton(
                    "✏️ Rename File",
                    callback_data="rename",
                )
            ],
            [
                InlineKeyboardButton(
                    "🎚️ Stream Tools",
                    callback_data="stream_help",
                )
            ],
        ]


        if (
            message.from_user
            and message.from_user.id in ADMIN_IDS
        ):

            buttons.append(
                [
                    InlineKeyboardButton(
                        "🆔 My ID",
                        callback_data="my_id",
                    )
                ]
            )


        await message.reply_text(

            "🤖 <b>Advanced File Renamer</b>\n\n"

            "Features:\n"
            "✏️ Rename File\n"
            "🔇 Remove Audio\n"
            "💬 Remove Subtitle\n"
            "🎬 Remove Video\n"
            "🎚️ Select Streams\n\n"

            "Use /rename to start.",

            reply_markup=InlineKeyboardMarkup(
                buttons
            ),
        )


    @app.on_callback_query(
        filters.regex("^my_id$")
    )
    async def my_id_callback(
        client,
        query,
    ):

        await query.answer(
            f"Your ID: {query.from_user.id}",
            show_alert=True,
        )


    @app.on_callback_query(
        filters.regex("^stream_help$")
    )
    async def stream_help_callback(
        client,
        query,
    ):

        await query.answer()

        await query.message.edit_text(

            "🎚️ <b>Stream Tools</b>\n\n"

            "🔇 Remove Audio\n"
            "Removes audio streams.\n\n"

            "💬 Remove Subtitle\n"
            "Removes subtitle streams.\n\n"

            "🎬 Remove Video\n"
            "Removes video streams.\n\n"

            "🎚️ Select Streams\n"
            "Choose exactly which streams to keep.\n\n"

            "All processing uses FFmpeg."
        )
