import re


def sanitize_filename(
    filename: str,
) -> str:

    filename = filename.strip()


    filename = re.sub(
        r'[<>:"/\\|?*\x00-\x1f]',
        "_",
        filename,
    )


    filename = re.sub(
        r"\s+",
        " ",
        filename,
    )


    if not filename:

        filename = "renamed_file"


    return filename[:240]
