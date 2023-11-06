# Telegram Crawler Setup

This document provides instructions on setting up and running the Telegram Crawler application in a Docker container. It also includes details on how to configure debugging for development in Visual Studio Code.

## Setting up Docker

Ensure Docker is available in your system's PATH with the following command:

```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

## Building the Docker Image

To build the Docker image for the Telegram Crawler, use the following command:

```bash
docker build -t telegram-crawler .
```

## Run and Debug in Docker

To facilitate running and debugging the Telegram Crawler inside a Docker container using Visual Studio Code, you need to create a `.vscode` directory in your project. This directory will contain the necessary configuration files.

### Configuration Files

#### launch.json

The `launch.json` file configures the debugging session. Create the file in the `.vscode` folder with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Docker Container",
            "type": "python",
            "request": "attach",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ],
            "port": 5678,
            "host": "localhost"
        }
    ]
}
```

tasks.json
The tasks.json file is used to build and run the Docker container. Create this file in the .vscode folder with the following content:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build and Run Docker",
            "type": "shell",
            "command": "docker run -p 5678:5678 -v \"${workspaceFolder}\":/app telegram-crawler",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

##  Running the Container
To run the container with the necessary port bindings, use the following command:

```bash
docker run -e TELEGRAM_API_ID='actual_api_id' -e TELEGRAM_API_HASH='actual_api_hash' -p 5678:5678 -it --rm --name telegram-debugging telegram-crawler
```

This command will start the container and remove it once the session is terminated. It also maps the local debugging port to the container's port.

## Debugging with debugpy
For debugging support within the container, you need to include debugpy in your Python application. Adjust your Python script to start a debugpy server, and ensure the Dockerfile installs debugpy.

## Additional Notes
Always ensure that your usage of the Telegram API is compliant with Telegram's Terms of Service.
Be cautious when automatically joining channels or groups to avoid any actions that might be perceived as spam.
Regularly review your development and debugging configurations to maintain a secure and efficient development environment.