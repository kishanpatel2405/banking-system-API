from fastapi import FastAPI


def start_app_handler(app: FastAPI):
    async def start() -> None:
        print("Application is starting up...")

    return start


def stop_app_handler(app: FastAPI):
    async def stop() -> None:
        print("Application is shutting down...")

    return stop
