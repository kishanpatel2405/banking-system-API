from fastapi import FastAPI


def start_app_handler(app: FastAPI):
    async def start() -> None:
        print("Application is starting up...")
        # Example: connect to DB or perform initialization tasks
        # db = Session(engine)
        # Do any other setup tasks here
    return start


# Function to run at shutdown (e.g., closing database connections, etc.)
def stop_app_handler(app: FastAPI):
    async def stop() -> None:
        # You can place cleanup logic here (e.g., database disconnection)
        print("Application is shutting down...")
        # Example: close DB connections
        # db.close()
        # Perform any other cleanup tasks here
    return stop
