# python-asyncio-kubernetes-template
A simple example of a micro-service written using Python Asyncio and hosted on Kubernetes (Google Container Engine)

This repository has two goals:
- Provide a complete example, and later short tutorial, on how to run a Python Asyncio based application on Kubernetes
  / Google Container Engine.
- Document my current understand of how best to structure the basics of a Python Asyncio application for use with
  Kubernetes. Specifically this refers to things like handling the shut down (SIGTERM) signal. It took me a while to
  figure this out so hopefully this example will save others time.

If you know of a better way to accomplish any of this please get in touch or submit a PR.
