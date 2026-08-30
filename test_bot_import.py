from bot import build_application


def main():
    application = build_application()

    assert application is not None

    print("BOT IMPORT TEST PASSED")


if __name__ == "__main__":
    main()
