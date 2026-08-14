import time


async def progress(
    current,
    total,
    message,
    action,
):
    now = time.time()

    if not hasattr(
        message,
        "_progress_time",
    ):
        message._progress_time = 0

    if (
        now - message._progress_time
        < 2
    ):
        return

    message._progress_time = now

    percent = (
        current * 100 / total
        if total
        else 0
    )

    done = (
        current / (1024 * 1024)
    )

    total_mb = (
        total / (1024 * 1024)
    )

    start_time = getattr(
        message,
        "_start_time",
        now,
    )

    elapsed = max(
        now - start_time,
        1,
    )

    speed = (
        current / elapsed
    )

    speed_mb = (
        speed / (1024 * 1024)
    )

    remaining = (
        total - current
    )

    eta = (
        remaining / max(speed, 1)
    )

    mins, secs = divmod(
        int(eta),
        60,
    )

    text = (
        f"{action}\n\n"
        f"📊 Progress: "
        f"{percent:.1f}%\n"
        f"📦 Size: "
        f"{done:.1f} MB / "
        f"{total_mb:.1f} MB\n"
        f"⚡ Speed: "
        f"{speed_mb:.2f} MB/s\n"
        f"⏱️ ETA: "
        f"{mins:02d}:{secs:02d}"
    )

    try:
        await message.edit_text(
            text
        )
    except Exception:
        pass
