# python-asyncio-kubernetes-template
A simple example of a micro-service written using Python Asyncio and hosted on Kubernetes (Google Container Engine)

This repository has two goals:
- Provide a complete example, and later short tutorial, on how to run a Python Asyncio based application on Kubernetes
  / Google Container Engine.
- Document my current understand of how best to structure the basics of a Python Asyncio application for use with
  Kubernetes. Specifically this refers to things like handling the shut down (SIGTERM) signal. It took me a while to
  figure this out so hopefully this example will save others time.

If you know of a better way to accomplish any of this please get in touch or submit a PR.

## Not 100% Complete Tutorial

### Create A Google Cloud Services Account and a Docker Cluster

All of this can be done in the Google Developers Console. Google has good docs on this.

For later steps you'll need to remember the project name, region/zone name and cluster name.

### Install the Google Cloud SDK

This provides the `gcloud` command and Kubernetes (`kubectl`).

`gcloud components list` shows which sub-components are installed. Just install all of them.

### Install and start Docker on your local machine.

####Fedora
```
dnf install docker
```
```
systemctl start docker.service
```
Note that the above only starts the docker service once. You need to enable the service if you want it to start on
every boot.
```
systemctl enable docker.service
```

### Build the container image
While inside the repository directory:
```
docker build .
```

When complete you will be able to see the image when listing the available Docker images.

`docker images`

### Tag the container image.
Now we need to tag the image to upload it to the Google Container Registry (GCR). Each Google Cloud project has it's own GCR name space. Replace the image ID and Google cloud project name in the example below.

```
docker tag -f IMAGE_ID gcr.io/PROJECT_ID/python-asyncio-kubernetes-template:latest
```

### Push the container image to GCR.
```
gcloud docker push gcr.io/PROJECT_ID/python-asyncio-kubernetes-template:latest
```

