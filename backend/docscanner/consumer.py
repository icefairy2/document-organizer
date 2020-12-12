# # Built in imports.
# import json
#
# # Third Party imports.
# from channels.exceptions import DenyConnection
# from channels.generic.websocket import AsyncWebsocketConsumer
# import asyncio
# import json
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# # Django imports.
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import AnonymousUser
#
# # Local imports.
# from docscanner.camera import VideoCamera
# from .models import Document
# from backend import settings
#
# import base64
# # from channels.routing import ProtocolTypeRouter
# # from django.core.asgi import get_asgi_application
#
# camera = VideoCamera()
#
# class LiveVideoFeedConsumer(AsyncConsumer):
#
#
#     async def websocket_connect(self, event):
#         print("Server connected: ", event)
#         await self.send({
#             "type": "websocket.accept"
#         })
#         # await asyncio.sleep(10)
#         # await self.send({
#         #     "type": "websocket.close"
#         # })
#
#     async def websocket_receive(self, event):
#         print("receive: ", event)
#
#     async def websocket_disconnect(self, event):
#         print("Server disconnected: ", event)
#
#
#
#     def onOpen(self):
#         print("WebSocket connection open.")
#
#         def hello():
#             # opening the image file and encoding in base64
#             frame = camera.get_cv_frame()
#             with open(frame, "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read())
#
#                 # printing the size of the encoded image which is sent
#                 print("Encoded size of the sent image: {0} bytes".format(len(encoded_string)))
#
#                 # sending the encoded image
#                 self.sendMessage(encoded_string.encode('utf8'))
#
#             hello()
#
#     def onMessage(self, payload, isBinary):
#         if isBinary:
#             print("Binary message received: {0} bytes".format(len(payload)))
#         else:
#             # printing the size of the encoded image which is received
#             print("Encoded size of the received image: {0} bytes".format(len(payload)))
#
#     def onClose(self, wasClean, code, reason):
#         print("WebSocket connection closed: {0}".format(reason))