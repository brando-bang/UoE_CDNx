# Overview
The VPN  Server acts as the gateway for content requests originating from the Clientside VPN Software. It is responsible for decrypting these requests, interacting with the Content Encryption Key Management Service to determine content availability, and relaying the appropriate response back to the client.
# Functionalities:
- Receives and decrypts content requests from Clientside VPN Software
- Checks with Content Encryption Key Management Service for content availability
- Forwards requests to the internet if necessary
- Forwards response back to Clientside VPN Software
# Endpoints:
- `/receiveRequest`: Receives encrypted content requests from Clientside VPN Software
- `/checkContentAvailability`: Checks with Content Encryption Key Management Service for content availability