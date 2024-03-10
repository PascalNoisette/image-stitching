
## Project Overview

The purpose of this project was to experiment with streamlit and docker for an image stitching experiment using OpenCV's newly added **Stitcher** class, which is based on methods proposed in David G. Lowe's [paper](http://matthewalunbrown.com/papers/ijcv2007.pdf).

The advanced demo of the capabilities of OpenCV sticher is explained here https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html, a stitching(_detailed).py script is supplied under the Apache 2 License and old version under the 3-clause BSD license.

A streamlit web interface is build around the Opencv script, the web interface was started by Moemen https://github.com/Mo-637/image-stitching.git under MIT License

![Demo](https://raw.githubusercontent.com/moeara/image-stitching/main/assets/demo.gif)


## Running the Demo Locally using Docker
To follow though with this demo, please make sure that you have 
[Git](https://github.com/git-guides/install-git) 
and 
[Docker](https://docs.docker.com/get-docker/) installed beforehand. 

```
docker run  -p8080:8080 --rm netpascal0123/image-stitching:latest
```
- Access the demo by visiting the following address in your preferred browser
```
http://0.0.0.0:8080/
```



## Build


- Build the docker image from source
```
git clone https://github.com/PascalNoisette/image-stitching.git
cd image-stitching
```

- Build the docker image
```
docker build -t 'stitcher:latest' .
```

- Run a container with the built image
```
docker container run -p 8080:8080 -d stitcher:latest
```
- Access the demo by visiting the following address in your preferred browser
```
http://0.0.0.0:8080/
```


## Running the Demo in your local workspace
If you prefer running the files in your workspace simply
- Install the prerequisites (Streamlit, OpenCV 3/4 and Numpy)
```
python3 -m pip install requirements.txt
```
- Run the web interface
```
cd demo
streamlit run gui.py
```
