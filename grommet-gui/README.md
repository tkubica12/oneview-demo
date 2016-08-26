# Grommet-GUI with OneView demo

This is simple demo application to demonstrate how Grommet can be used to create responsive GUI for your applications and also to build GUI on top of OneView APIs. This demo presents simple web page where user can anonymously create Storage Volume and number of Volumes is displayed in meter gadget. Idea is to demonstrate that OneView APIs are gateway to your infrastructure and make it very easy to build apps on top.

![alt text](https://github.com/tkubica12/oneview-demo/blob/master/grommet-gui/grommet-gui-screen.PNG "grommet-gui screenshot")


Docker image is available to make demo as easy as possible. On your Docker host run the following and use environmental variables to setup connectivity to your OneView appliance:

```
docker run -e "OV_USERNAME=Administrator" -e "OV_PASSWORD=HPEnet123" -e "OV_SERVER=192.168.89.100" -e "OV_STORAGE_POOL=CPG-SSD" -d -p 80:80 -p 3000:3000 --name myapp tomaskubica/grommet-gui
```

If you have done any changes to source files and would like to build your own Docker image with that, use Dockerfile in project root folder to build it.

## Backend service
This is simple Python application which servers as backend. Easiest way to run it is use this Docker container and provide environmental variables with connection details to your OneView appliance.

If you want to build this yourself, install Python2, Bottle and python-hpOneView library.

## Frontend (Grommet GUI)
Simple GUI is written with Node.JS and Grommet (based on React). For testing download Grommet and then run "gulp dev" in frontend folder. When you are done with changes run "gulp dist" to export your application to dist folder. Then take its content (static web content) and place it on web server of your choice.

## Packaging as Docker image
If you made changes to frontend or backend and want to build new Docker image first make gulp distribute files and then build container in main grommet-gui folder.

```
docker build -t mynewimage .
```
