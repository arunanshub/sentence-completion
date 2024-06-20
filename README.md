# sentence-completion

## Running in Docker

1. Install [NVIDIA container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for GPU support in containers. Follow NVIDIA's guide to get started.

2. Build the docker image: `docker build . -t sentence-completion:latest`

3. Launch the image: `docker run -t --rm --runtime nvidia --gpus all -p 8000:8000 sentence-completion:latest`
