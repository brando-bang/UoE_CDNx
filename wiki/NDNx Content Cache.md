# Overview:
The Network-local Content Cache is designed to store encrypted content assets within the VPN provider's network. Its primary role is to serve content directly to clients upon request, thereby reducing latency and improving the efficiency of content delivery within the CCNX system.
# Functionalities:
- Stores encrypted content
- Receives and responds to requests for encrypted content from Clientside VPN Software
# Endpoints:
- `/getContent`: Returns encrypted content upon request
- `/hasContent`: Allows VPN server to check if content exists in the cache