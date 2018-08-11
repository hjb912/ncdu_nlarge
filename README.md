![](https://img.shields.io/badge/python-3.6.5-orange.svg)

This repo is a wrapper of ncdu.
## 目标

找出前n个大文件，列出其路径。

## 如何使用

首先, 在目标机器安装 [ncdu] 和 [my repo]

```bash
$ wget http://dev.yorhel.nl/download/ncdu-1.12.tar.gz
$ tar -xzvf ncdu-1.12.tar.gz
$ cd ncdu-1.12
$ ./configure --prefix=/usr
```

If, some err.

```bash
$ checking for ncurses.h... no
configure: error: required header file not found
```

Install the dependencies.

```bash
$ yum install ncurses-devel ncurses
```

Now, make.

```bash
$ make && make install
$ ./configure --prefix=/usr
$ ncdu
```
Then, install [my repo](https://github.com/hjb912/ncdu_nlarge.git)

```bash
$ git clone https://github.com/hjb912/ncdu_nlarge
```



## 用法

1.如果目标机器硬盘空间还有余，则可以直接在上面运行。

```bash
$ cd /ncdu_nlarge
$ python extract.py -p '/' -n 10
```

参数说明

- `-p` – 目标检索开始路径
- `-n` – 检索出当前最大n个数量的文件信息


2.如果目标机器硬盘空间非常紧张，则我们可以把结果导出来，在自己本地分析。
这样自己本地只需要安装[my repo]即可。

```bash
$ cd /ncdu_nlarge
$ python extract.py -p '/' -n 10 -ssh 'ssh -C root@1.2.3.4 -p 12345'
```

参数说明

- `-ssh` – 通过ssh获取远端机器信息，导出文件到本地。


## 测试
本机测试

配置：mbp，cpu:2.7GHz，mem:8GB，hd：128GB

扫描disk：93.19 GB，1722492 files，中间导出文件19.7MB，用时296.76s。
