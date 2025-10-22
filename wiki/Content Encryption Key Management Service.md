# Overview:
The Content Encryption Key Management Service is a critical backend component responsible for securely managing and providing the necessary encryption keys. It serves the VPN Entrypoint Server by supplying content encryption keys and ID encryption keys, which are essential for both verifying content availability and enabling decryption by the clientside software.
# Functionalities:
- Manages encryption keys for content cached in Network-local Content Cache
- Provides content encryption keys and id encryption keys to VPN Entrypoint Server
# Endpoints:
- `/getEncryptionKeys`: Provides encryption keys for requested content
