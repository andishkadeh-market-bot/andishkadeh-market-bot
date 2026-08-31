import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import bot
from core import database


@pytest.fixture
def isolated_database(tmp_path, monkeypatch):
    db_path = tmp_path / "bot_integration.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        db_path,
    )

    database.init_database()

    return db_path


def test_initialize_core(
    isolated_database,
):
    bot.initialize_core()

    with database.get_connection() as connection:

        connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()

        connection.execute(
            "SELECT COUNT(*) FROM lesson_progress"
        ).fetchone()

        connection.execute(
            "SELECT COUNT(*) FROM quiz_attempts"
        ).fetchone()


def test_start_registers_user_and_shows_menu(
    isolated_database,
):
    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 123456
    update.effective_user.username = "integration_user"
    update.effective_user.first_name = "Integration"
    update.effective_user.last_name = "Test"

    update.message = MagicMock()

    with patch(
        "bot.show_main_menu",
        new=AsyncMock(),
    ) as show_menu:

        asyncio.run(
            bot.start(
                update,
                context,
            )
        )

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (123456,),
        ).fetchone()

    assert row is not None

    assert (
        row["username"]
        == "integration_user"
    )

    assert (
        row["first_name"]
        == "Integration"
    )

    assert (
        row["last_name"]
        == "Test"
    )

    show_menu.assert_awaited_once_with(
        update,
        context,
    )


def test_start_updates_existing_user(
    isolated_database,
):
    database.upsert_user(
        telegram_id=123457,
        username="old_name",
        first_name="Old",
        last_name="User",
    )

    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 123457
    update.effective_user.username = "new_name"
    update.effective_user.first_name = "New"
    update.effective_user.last_name = "User"

    update.message = MagicMock()

    with patch(
        "bot.show_main_menu",
        new=AsyncMock(),
    ):

        asyncio.run(
            bot.start(
                update,
                context,
            )
        )

    with database.get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (123457,),
        ).fetchone()

    assert row is not None

    assert (
        row["username"]
        == "new_name"
    )

    assert (
        row["first_name"]
        == "New"
    )


def test_start_without_user_does_nothing(
    isolated_database,
):
    update = MagicMock()
    context = MagicMock()

    update.effective_user = None

    with patch(
        "bot.show_main_menu",
        new=AsyncMock(),
    ) as show_menu:

        asyncio.run(
            bot.start(
                update,
                context,
            )
        )

    show_menu.assert_not_awaited()


def test_start_without_message_does_nothing(
    isolated_database,
):
    update = MagicMock()
    context = MagicMock()

    update.effective_user = MagicMock()
    update.effective_user.id = 123458

    update.message = None

    with patch(
        "bot.show_main_menu",
        new=AsyncMock(),
    ) as show_menu:

        asyncio.run(
            bot.start(
                update,
                context,
            )
        )

    show_menu.assert_not_awaited()


def test_start_handles_database_error(
    isolated_database,
):
    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 123459
    update.effective_user.username = "error_user"
    update.effective_user.first_name = "Error"
    update.effective_user.last_name = "Test"

    update.message = MagicMock()

    update.message.reply_text = AsyncMock()

    with patch(
        "bot.upsert_user",
        side_effect=RuntimeError(
            "database failure"
        ),
    ):

        asyncio.run(
            bot.start(
                update,
                context,
            )
        )

    update.message.reply_text.assert_awaited_once()


def test_build_application_registers_handlers(
    isolated_database,
):
    with patch(
        "bot.BOT_TOKEN",
        "test-token",
    ):

        with patch.object(
            bot,
            "initialize_core",
        ) as initialize_core:

            application = (
                bot.build_application()
            )

    initialize_core.assert_called_once()

    handlers = application.handlers

    command_handlers = [
        handler
        for handler_list in handlers.values()
        for handler in handler_list
        if handler.__class__.__name__
        == "CommandHandler"
    ]

    callback_handlers = [
        handler
        for handler_list in handlers.values()
        for handler in handler_list
        if handler.__class__.__name__
        == "CallbackQueryHandler"
    ]

    assert len(command_handlers) == 1
    assert len(callback_handlers) == 1


def test_build_application_requires_token(
    isolated_database,
):
    with patch(
        "bot.BOT_TOKEN",
        "",
    ):

        with pytest.raises(
            RuntimeError,
            match="BOT_TOKEN is not configured",
        ):

            bot.build_application()


def test_error_handler_logs_error():
    context = MagicMock()

    context.error = RuntimeError(
        "test error"
    )

    asyncio.run(
        bot.error_handler(
            MagicMock(),
            context,
        )
    )
