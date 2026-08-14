import asyncio
import json
import os
import tempfile

from config import TEMP_DIR


class FFmpegError(
    RuntimeError
):
    pass


async def run_command(
    command,
):

    process = (
        await asyncio.create_subprocess_exec(
            *command,

            stdout=(
                asyncio.subprocess.PIPE
            ),

            stderr=(
                asyncio.subprocess.PIPE
            ),
        )
    )


    stdout, stderr = (
        await process.communicate()
    )


    if process.returncode != 0:

        error = stderr.decode(
            "utf-8",
            errors="replace",
        )


        raise FFmpegError(
            error[-6000:]
        )


    return stdout.decode(
        "utf-8",
        errors="replace",
    )


async def check_ffmpeg():

    await run_command(
        [
            "ffmpeg",
            "-version",
        ]
    )


    await run_command(
        [
            "ffprobe",
            "-version",
        ]
    )


async def probe(
    file_path,
):

    output = await run_command(
        [
            "ffprobe",

            "-v",
            "error",

            "-print_format",
            "json",

            "-show_streams",

            "-show_format",

            str(file_path),
        ]
    )


    return json.loads(
        output
    )


def stream_summary(
    info,
):

    result = []


    for stream in info.get(
        "streams",
        []
    ):

        tags = (
            stream.get("tags")
            or {}
        )


        result.append(
            {
                "index": stream.get(
                    "index"
                ),

                "type": stream.get(
                    "codec_type"
                ),

                "codec": stream.get(
                    "codec_name"
                ),

                "language": tags.get(
                    "language",
                    "",
                ),

                "title": tags.get(
                    "title",
                    "",
                ),
            }
        )


    return result


async def remove_audio(
    input_file,
    output_file,
):

    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_file),

        "-map",
        "0",

        "-map",
        "-0:a",

        "-map_metadata",
        "0",

        "-c",
        "copy",

        str(output_file),
    ]


    await run_command(
        command
    )


    return output_file


async def remove_subtitles(
    input_file,
    output_file,
):

    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_file),

        "-map",
        "0",

        "-map",
        "-0:s",

        "-map_metadata",
        "0",

        "-c",
        "copy",

        str(output_file),
    ]


    await run_command(
        command
    )


    return output_file


async def remove_video(
    input_file,
    output_file,
):

    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_file),

        "-map",
        "0",

        "-map",
        "-0:v",

        "-map_metadata",
        "0",

        "-c",
        "copy",

        str(output_file),
    ]


    await run_command(
        command
    )


    return output_file


async def select_streams(
    input_file,
    output_file,
    video=True,
    audio_indices=None,
    subtitle_indices=None,
):

    audio_indices = (
        audio_indices
        or []
    )

    subtitle_indices = (
        subtitle_indices
        or []
    )


    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_file),
    ]


    if video:

        command.extend(
            [
                "-map",
                "0:v:0",
            ]
        )


    for index in audio_indices:

        command.extend(
            [
                "-map",
                f"0:a:{int(index)}",
            ]
        )


    for index in subtitle_indices:

        command.extend(
            [
                "-map",
                f"0:s:{int(index)}",
            ]
        )


    if len(command) == 4:

        raise ValueError(
            "No streams selected."
        )


    command.extend(
        [
            "-map_metadata",
            "0",

            "-c",
            "copy",

            str(output_file),
        ]
    )


    await run_command(
        command
    )


    return output_file


async def process(
    input_file,
    output_file,

    remove_audio_streams=False,

    remove_subtitle_streams=False,

    remove_video_streams=False,

    video=True,

    audio_indices=None,

    subtitle_indices=None,
):

    if (
        audio_indices is not None
        or subtitle_indices is not None
    ):

        return await select_streams(

            input_file,

            output_file,

            video=video,

            audio_indices=audio_indices,

            subtitle_indices=subtitle_indices,
        )


    maps = [

        "-map",
        "0",
    ]


    if remove_audio_streams:

        maps.extend(
            [
                "-map",
                "-0:a",
            ]
        )


    if remove_subtitle_streams:

        maps.extend(
            [
                "-map",
                "-0:s",
            ]
        )


    if remove_video_streams:

        maps.extend(
            [
                "-map",
                "-0:v",
            ]
        )


    if len(maps) == 2:

        raise ValueError(
            "No processing operation selected."
        )


    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_file),

        *maps,

        "-map_metadata",
        "0",

        "-c",
        "copy",

        str(output_file),
    ]


    await run_command(
        command
    )


    return output_file


def make_temp_path(
    extension=".mkv",
):

    fd, path = (
        tempfile.mkstemp(
            suffix=extension,
            dir=TEMP_DIR,
        )
    )


    os.close(fd)


    return path
