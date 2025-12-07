# Purpose of Repo
This repo contains the service code and infrastructure-as-code for deploying a simulation of an internet user and a vpn service. This allows for testing the relative performance of NDNx as compared to a combination of using VPNs, CDNs, both, or neither. It contains hardcoded endpoints that accurately stub the different sequences involved in (and outside of) NDNx and reporting in order to analyze internet performance.

# High Level Diagram
![HLD](graphics/NDNxDiagram.png)
Fig. 1: This HLD shows the overall sequence of how the NDNx content retrieval works. The component-to-component interactions will be broken down further.

# Sequence Diagrams
![sequence diagram for cache hit](graphics/sequenceDiagram1.png)
Fig. 2: flow chart for content available in NDNx cache

![sequence diagram for cache miss](graphics/sequenceDiagram2.png)
Fig. 3: flow chart for content that is not in the cache
