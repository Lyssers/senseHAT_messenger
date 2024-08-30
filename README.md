# A Mesenger for your SenseHAT!

This consists of two main components:

1) API endpoint using FastAPI and Uvicorn running on your raspberry pi to do everything with the SenseHAT
2) Static HTML Webpage with an input text field and button that makes a simple GET request with message as URL parameter and rudimentary ugly display of returned messages

Edit both to point to the correct domains you're going to be hosting under and host on your favourite web server (lighttpd config and deployment shell script attached for backup and convenience)

SenseHAT:

![image](https://github.com/Lyssers/senseHAT_messenger/blob/main/video_2024-08-30_14-56-02.gif)

Web:

![image](https://github.com/user-attachments/assets/30201446-e903-46cd-ad31-8ceb71e9a4e1)
