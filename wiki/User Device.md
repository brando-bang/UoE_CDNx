# Overview
The User Device Stack simulates a VPN user's device. This simulates the primary entrypoint of an internet user whether they are using a VPN, NDNx, a CDN, or nothing at all. The endpoints return time stats in order to compare the relative performance of content retrieval strategies
# Endpoints:
- `/heartbeat`: a healthcheck endpoint used to check for a successful deployment of the stack
- `/download_direct`: this endpoint downloads the 10mb testing asset directly from the nforce mirror (which does not employ a CDN) and sets a baseline for internet performance
- `/download_cdn`: this endpoint downloads the same 10mb testing asset from a CDN which sets a baseline for a high performance content request
- `/use_vpn`: this endpoint is used to access the VPN service stack, which will then either access the nforce mirror or the cdn and return the content with end-to-end-encryption