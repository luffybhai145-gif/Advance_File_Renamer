import os
import asyncio

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import (
    ADMIN_IDS,
    TEMP_DIR,
    MAX_CONCURRENT_FFMPEG,
)

from utils.ffmpeg import (
    probe,
    stream_summary,
    process,
    FFmpegError,
)

from utils.filename import sanitize_filename


SESSIONS = {}


FFMPEG_SEMAPHORE = asyncio.Semaphore(
    MAX_CONCURRENT_FFMPEG
)


def main_menu():

    return InlineKeyboardMarkup(
        [

            [
                InlineKeyboardButton(
                    "✏️ Rename",
                    callback_data="act_rename",
                )
            ],

            [
                InlineKeyboardButton(
                    "🔇 Remove Audio",
                    callback_data="act_audio",
                ),

                InlineKeyboardButton(
                    "💬 Remove Subtitle",
                    callback_data="act_subtitle",
                ),
            ],

            [
                InlineKeyboardButton(
                    "🎬 Remove Video",
                    callback_data="act_video",
                )
            ],

            [
                InlineKeyboardButton(
                    "🎚️ Select Streams",
                    callback_data="act_select",
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="act_cancel",
                )
            ],

        ]
    )


def stream_menu(info, selected):

    rows = []


    for stream in info.get(
        "streams",
        []
    ):

        index = stream.get(
            "index"
        )

        stream_type = stream.get(
            "codec_type",
            "unknown",
        )

        codec = stream.get(
            "codec_name",
            "",
        )

        language = ""

        tags = stream.get(
            "tags"
        )

        if tags:

            language = tags.get(
                "language",
                "",
            )


        mark = (
            "✅"
            if index in selected
            else "⬜"
        )


        text = (
            f"{mark} #{index} "
            f"{stream_type} "
            f"{codec}"
        )


        if language:

            text += (
                f" [{language}]"
            )


        rows.append(
            [
                InlineKeyboardButton(
                    text[:60],
                    callback_data=f"stream_{index}",
                )
            ]
        )


    rows.append(
        [
            InlineKeyboardButton(
                "🚀 Process Selected",
                callback_data="process_selected",
            )
        ]
    )


    rows.append(
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="act_cancel",
            )
        ]
    )


    return InlineKeyboardMarkup(
        rows
    )


def get_media_file_name(message):

    if message.document:

        return (
            message.document.file_name
            or "file"
        )


    if message.video:

        return (
            message.video.file_name
            or "video.mkv"
        )


    if message.audio:

        return (
            message.audio.file_name
            or "audio.mka"
        )


    return "file"


def selected_streams(
    info,
    selected_indexes,
):

    video = False

    audio = []

    subtitles = []


    audio_count = 0

    subtitle_count = 0


    for stream in info.get(
        "streams",
        []
    ):

        stream_index = stream.get(
            "index"
        )

        stream_type = stream.get(
            "codec_type"
        )


        if stream_type == "video":

            if stream_index in selected_indexes:

                video = True


        elif stream_type == "audio":

            if stream_index in selected_indexes:

                audio.append(
                    audio_count
                )

            audio_count += 1


        elif stream_type == "subtitle":

            if stream_index in selected_indexes:

                subtitles.append(
                    subtitle_count
                )

            subtitle_count += 1


    return (
        video,
        audio,
        subtitles,
    )


def register(app, db):

    @app.on_message(
        filters.command("rename")
        & filters.private
    )
    async def rename_command(
        client,
        message,
    ):

        if (
            not message.from_user
            or message.from_user.id
            not in ADMIN_IDS
        ):

            await message.reply_text(
                "❌ Unauthorized."
            )

            return


        SESSIONS[
            message.from_user.id
        ] = {

            "stage": "file",

            "message": None,

            "path": None,

            "info": None,

            "action": None,

            "selected": set(),

        }


        await message.reply_text(

            "📤 <b>Send your media file.</b>\n\n"

            "Supported:\n"
            "• Video\n"
            "• Audio\n"
            "• Document"

        )


    @app.on_callback_query(
        filters.regex("^rename$")
    )
    async def rename_button(
        client,
        query,
    ):

        if (
            query.from_user.id
            not in ADMIN_IDS
        ):

            await query.answer(
                "Unauthorized.",
                show_alert=True,
            )

            return


        SESSIONS[
            query.from_user.id
        ] = {

            "stage": "file",

            "message": None,

            "path": None,

            "info": None,

            "action": None,

            "selected": set(),

        }


        await query.message.reply_text(
            "📤 Send your media file."
        )

        await query.answer()


    @app.on_message(
        filters.private
        & (
            filters.document
            | filters.video
            | filters.audio
        )
    )
    async def receive_file(
        client,
        message,
    ):

        uid = (
            message.from_user.id
            if message.from_user
            else 0
        )


        if (
            uid not in ADMIN_IDS
            or uid not in SESSIONS
        ):

            return


        session = SESSIONS[uid]


        if session["stage"] != "file":

            return


        status = await message.reply_text(
            "⬇️ Downloading..."
        )


        path = None


        try:

            path = await client.download_media(
                message,
                file_name=TEMP_DIR + "/",
            )


            session["path"] = path

            session["message"] = message


            await status.edit_text(
                "🔎 Detecting streams..."
            )


            info = await probe(
                path
            )


            session["info"] = info

            session["stage"] = "action"


            summary = stream_summary(
                info
            )


            text = (
                "🎚️ <b>Detected Streams</b>\n\n"
            )


            for stream in summary:

                text += (
                    f"#{stream['index']} | "
                    f"{stream['type']} | "
                    f"{stream['codec'] or '-'}"
                )


                if stream["language"]:

                    text += (
                        f" | {stream['language']}"
                    )


                text += "\n"


            text += (
                "\nChoose an operation:"
            )


            await status.edit_text(
                text,
                reply_markup=main_menu(),
            )


        except Exception as error:

            await status.edit_text(

                "❌ <b>Error</b>\n\n"
                f"<code>{str(error)[-3000:]}</code>"
            )


            if (
                path
                and os.path.exists(path)
            ):

                os.remove(path)


    @app.on_callback_query(
        filters.regex("^act_")
    )
    async def action_callback(
        client,
        query,
    ):

        uid = query.from_user.id


        if (
            uid not in ADMIN_IDS
            or uid not in SESSIONS
        ):

            await query.answer(
                "No active job.",
                show_alert=True,
            )

            return


        session = SESSIONS[uid]


        action = query.data[4:]


        if action == "cancel":

            await cleanup(
                uid
            )

            await query.message.edit_text(
                "❌ Cancelled."
            )

            await query.answer()

            return


        if action == "rename":

            session["action"] = (
                "rename_only"
            )


        elif action == "audio":

            session["action"] = (
                "remove_audio"
            )


        elif action == "subtitle":

            session["action"] = (
                "remove_subtitle"
            )


        elif action == "video":

            session["action"] = (
                "remove_video"
            )


        elif action == "select":

            session["action"] = (
                "select"
            )

            session["stage"] = (
                "selecting"
            )


            await query.message.edit_text(

                "🎚️ <b>Select Streams</b>\n\n"
                "Tap the streams you want to keep.\n"
                "Then press Process.",

                reply_markup=stream_menu(
                    session["info"],
                    session["selected"],
                ),
            )


            await query.answer()

            return


        session["stage"] = (
            "new_name"
        )


        await query.message.edit_text(

            "✏️ Send the new filename.\n\n"
            "Example:\n"
            "<code>Episode 01.mkv</code>"
        )


        await query.answer()


    @app.on_callback_query(
        filters.regex("^stream_")
    )
    async def stream_toggle(
        client,
        query,
    ):

        uid = query.from_user.id


        session = SESSIONS.get(
            uid
        )


        if not session:

            await query.answer(
                "No active job.",
                show_alert=True,
            )

            return


        index = int(
            query.data.split(
                "_",
                1
            )[1]
        )


        if (
            index
            in session["selected"]
        ):

            session[
                "selected"
            ].remove(index)

            text = "Unselected"

        else:

            session[
                "selected"
            ].add(index)

            text = "Selected"


        await query.message.edit_reply_markup(
            stream_menu(
                session["info"],
                session["selected"],
            )
        )


        await query.answer(
            text
        )


    @app.on_callback_query(
        filters.regex(
            "^process_selected$"
        )
    )
    async def process_selected(
        client,
        query,
    ):

        uid = query.from_user.id


        session = SESSIONS.get(
            uid
        )


        if not session:

            await query.answer(
                "No active job.",
                show_alert=True,
            )

            return


        if not session["selected"]:

            await query.answer(
                "Select at least one stream.",
                show_alert=True,
            )

            return


        session["stage"] = (
            "new_name"
        )

        session["action"] = (
            "select"
        )


        await query.message.reply_text(

            "✏️ Send the output filename.\n\n"
            "Example:\n"
            "<code>Episode 01.mkv</code>"
        )


        await query.answer()


    @app.on_message(
        filters.private
        & filters.text
        & ~filters.command(
            [
                "start",
                "rename",
            ]
        )
    )
    async def new_name(
        client,
        message,
    ):

        uid = (
            message.from_user.id
            if message.from_user
            else 0
        )


        session = SESSIONS.get(
            uid
        )


        if not session:

            return


        if session["stage"] != "new_name":

            return


        output_name = (
            sanitize_filename(
                message.text
            )
        )


        input_path = (
            session["path"]
        )


        extension = os.path.splitext(
            output_name
        )[1]


        if not extension:

            output_name += (
                os.path.splitext(
                    input_path
                )[1]
            )


        output_path = os.path.join(
            TEMP_DIR,
            f"output_{uid}_{output_name}",
        )


        status = await message.reply_text(
            "⚙️ Processing..."
        )


        try:

            async with (
                FFMPEG_SEMAPHORE
            ):

                if (
                    session["action"]
                    == "rename_only"
                ):

                    os.replace(
                        input_path,
                        output_path,
                    )

                    final_path = (
                        output_path
                    )


                elif (
                    session["action"]
                    == "remove_audio"
                ):

                    final_path = (
                        await process(
                            input_path,
                            output_path,
                            remove_audio_streams=True,
                        )
                    )


                elif (
                    session["action"]
                    == "remove_subtitle"
                ):

                    final_path = (
                        await process(
                            input_path,
                            output_path,
                            remove_subtitle_streams=True,
                        )
                    )


                elif (
                    session["action"]
                    == "remove_video"
                ):

                    final_path = (
                        await process(
                            input_path,
                            output_path,
                            remove_video_streams=True,
                        )
                    )


                elif (
                    session["action"]
                    == "select"
                ):

                    video, audio, subtitles = (
                        selected_streams(
                            session["info"],
                            session["selected"],
                        )
                    )


                    final_path = (
                        await process(
                            input_path,
                            output_path,
                            video=video,
                            audio_indices=audio,
                            subtitle_indices=subtitles,
                        )
                    )


                else:

                    raise ValueError(
                        "Unknown action."
                    )


            await status.edit_text(
                "⬆️ Uploading..."
            )


            await client.send_document(

                chat_id=uid,

                document=final_path,

                file_name=output_name,

                caption=(
                    "✅ <b>Processing completed.</b>"
                ),
            )


            await status.delete()


        except (
            FFmpegError,
            ValueError,
            OSError,
        ) as error:

            await status.edit_text(

                "❌ <b>Processing failed.</b>\n\n"

                f"<code>"
                f"{str(error)[-4000:]}"
                f"</code>"
            )


        finally:

            for path in (
                session.get("path"),
                output_path,
            ):

                if (
                    path
                    and os.path.exists(path)
                ):

                    try:

                        os.remove(
                            path
                        )

                    except OSError:

                        pass


            SESSIONS.pop(
                uid,
                None,
            )


    async def cleanup(uid):

        session = SESSIONS.pop(
            uid,
            None,
        )


        if not session:

            return


        path = session.get(
            "path"
        )


        if (
            path
            and os.path.exists(path)
        ):

            try:

                os.remove(path)

            except OSError:

                pass
