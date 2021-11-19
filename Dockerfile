#
#
#
## Base images 基础镜像
#FROM python:3.9.7-bullseye
#
##MAINTAINER 维护者信息
#MAINTAINER huhu
#
## 设置语言 必须设置，否则下载某些python依赖包报错
#ENV LANG C.UTF-8
#ENV LANGUAGE C.UTF-8
#ENV LC_ALL C.UTF-8
#
#
##指定工作目录，若无，则自动创建
#WORKDIR /root/app
#
#COPY . .
#
#RUN pip install -r requirements.txt
#
##EXPOSE 映射端口
#EXPOSE 9000 9001
#
## 运行服务
##CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--log-level", "info"]
#CMD ['gunicorn',"-c","gunicorn.conf.py","main:app"]


#1.从官方python基础镜像开始
FROM python:3.9

#2.将当前目录设置为/code
#这是放置requirements.txt文件和应用程序目录的地方
WORKDIR /code

#3.先复制requirements.txt文件
#由于这个文件不经常更改. Docker会检测它并在这一步使用缓存,也为下一步启用缓存
COPY ./requirement.txt /code/requirements.txt

#4.运行pip命令安装依赖
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#5.复制FastAPI项目代码
COPY ./app /code/app

#6.运行服务
CMD ['uvicorn',"app.main:app","--host","0.0.0.0","--port","8001"]
