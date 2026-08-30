import asyncio

from bot import build_application


async def main():
    application = build_application()

    await application.initialize()

    print("BOT STARTUP TEST PASSED")

    await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
