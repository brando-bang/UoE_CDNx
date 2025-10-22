# Overview
The Clientside VPN Software is a crucial component of the CCNX system, responsible for encrypting content requests and handling the retrieval of encrypted content from the Network-local Content Cache.
# Functionalities:
- Encrypts content requests using user's VPN encryption key
- Sends encrypted requests to VPN Entrypoint Server
- Receives response regarding content availability
- Requests encrypted content from Network-local Content Cache if available
- Decrypts received content using content encryption key
# Endpoints:
- `/sendRequest`: Sends encrypted content request to VPN Entrypoint Server
- `/requestContent`: Requests encrypted content from Network-local Content Cache