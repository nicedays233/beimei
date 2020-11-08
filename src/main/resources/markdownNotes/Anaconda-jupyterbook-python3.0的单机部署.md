## Anaconda-jupyterbook-python3.0的单机部署与spark相连接

### 为什么要安装Anaconda？

> - python自身缺少numpy、matplotlib、scipy、scikit-learn....等一系列包du，需要安装pip来导入这些包才能进行相应运算Anaconda(开源的Python包管理器)是一个python发行版，包含了conda、Python等180多个科学包及其依赖项。包含了大量的包，使用anaconda无需再去额外安装所需包。
> - IPython 是一个 python 的交互式 shell，比默认的python shell 好用得多，支   持变量自动补全，自动缩进，支持 bash shell 命令，内置了许多很有用的功能和  函数。而Anaconda Prompt 是一个Anaconda的终端，可以便捷的操作conda  环境。

### 安装步骤-重点与spark分布式系统的结合：

#### 第一步：首先你要预先安装过spark

#### 第二步：在/etc/profile配置spark环境

```shell
vi /etc/profile
```

- 添加环境配置

```shell
export SPARK_HOME=/opt/soft/spark234
export SPARK_CONF_DIR=$SPARK_HOME/conf
export PATH=$PATH:$SPARK_HOME/bin
```

```shell
source /etc/profile
```

#### 第三步：安装bzip2

```shell
yum install -y bzip2 # 此步不执行安装anaconda会报错
```

#### 第四步：linux下运行anaconda3.5.1脚本

- 下载地址：

```shell
bash /opt/Anaconda3-5.1.0-Linux-x86_64.sh
```

> 根据提示回车和yes，最后的vscode编辑器选择no不安装

#### 第五步：生成jupyter配置文件

- 找到/root/anaconda3/bin进入

```shell
cd /root/anaconda3/bin
```

- 运行命令

```shell
./jupyter notebook --generate-config
```

- 当前目录运行命令生成jupyter登陆密码

```shell
./ipython
```

- python界面下

```python
 from notebook.auth import passwd
 passwd()
```

> 输入你的密码后 生成一个sha1:xxxxx 用记事本链贴好

#### 第六步：修改jupyter_notebook_config.py文件

```shell
 vi /root/.jupyter/jupyter_notebook_config.py 
```

```python
c.NotebookApp.allow_root=True
c.NotebookApp.ip='*'
c.NotebookApp.open_browser=False
c.NotebookApp.password=u'加入刚才生成的密码'
c.NotebookApp.port=7070 #此端口为不使用pyspark的端口
```

#### 第七步：配置全局变量

```shell
vi /etc/profile
```

```shell
#anaconda3 environment
export ANACONDA_HOME=/root/anaconda3
export PATH=$PATH:$ANACONDA_HOME/bin
export PYSPARK_DRIVER_PYTHON=jupyter-notebook
export PYSPARK_DRIVER_PYTHON_OPTS=" --ip=0.0.0.0 --port=8888"

```

```shell
source /etc/profile
```



#### 第八步：选择进入的界面

- 进入普通python环境

```shell
jupyter notebook --allow-root
```

> 输入命令提示对应得ip+端口号可以登陆了

![image-20200812192013566](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200812192013566.png)

- 进入pyspark环境

```shell
pyspark
```

> 输入命令提示对应得ip+端口号可以登陆了

![image-20200812194320727](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200812194320727.png)