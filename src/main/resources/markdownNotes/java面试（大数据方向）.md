## java面试（大数据方向）

### 1.数组（二维数组）



### 2.排序（冒泡，快速）

```java
# 快排
int[] arr = {2,4,56,1,7,7}
public void quick(int low, int high){
    int lo = low; int hi = high;
    if (lo >= hi) {
        return;
    }
    boolean flag = false;
    while (lo < hi) {
        if (arr[lo] > arr[hi]) {
            int temp = arr[lo];
            arr[lo] = arr[hi];
            arr[hi] = temp;
            flag = !flag;
        }
        if (flag){
            lo++;
        }else {            
            hi--;
        }
        lo--;hi++;
    }
    quick(low, lo);
    quick(hi, high);
}
```

```java
# 冒泡
public void maopao(int[] arr) {
    for (int i = 0; i < arr.length; ++i) {
        for (int j = 0; j < arr.length - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```



### 3.树结构处理

### 4.集合

#### ArrayList

```java
public class MyList<T> {
	private Object[] eles={};
	private Object[] elements;
	private int size;
	private final int DEFALUT_CAPACITY= 10;

	public MyList(){
		this.elements = eles;
	}
	public MyList(int size) throws  Exception{
		if (size < 0) {
			throw new Exception("xxx");
		}else if (size == 0){
			this.elements = eles;
		}{
			this.elements = new Object[size];
		}
	}

	public void add(T t) {
		// 先检查数组容量
		checkCapacity(size + 1);
		this.elements[size++] = t;
	}

	public void remove(int index) throws Exception{
		if (index < 0 || index >= this.elements.length){
			throw new Exception("xxxx");
		}
		int afterlen = this.elements.length - index - 1;
		System.arraycopy(this.elements, index + 1, this.elements, index, afterlen);
		this.elements[--size] = null;
	}

	public void checkCapacity(int i){
		int newCapacity = 0;
		if(this.elements == eles) {
			newCapacity = DEFALUT_CAPACITY;
		}
		if (i < this.elements.length - 1) {
			return;
		}else {
			if (newCapacity != 0) {
				this.elements = new Object[newCapacity];
			}else {
				// 重新计算容量
				int oldCapacity = this.elements.length;
				newCapacity = oldCapacity + (oldCapacity >> 1);

				Object[] newArr = new Object[newCapacity];
				System.arraycopy(this.elements, 0, newArr, 0, this.elements.length);
				this.elements = newArr;
			}
		}

	}
	public static void main(String[] args) {

		ArrayList r = new  ArrayList();
	}
}
```

#### HashMap

```java
public class MyList<T> {
	private Object[] eles={};
	private Object[] elements;
	private int size;
	private final int DEFALUT_CAPACITY= 10;

	public MyList(){
		this.elements = eles;
	}
	public MyList(int size) throws  Exception{
		if (size < 0) {
			throw new Exception("xxx");
		}else if (size == 0){
			this.elements = eles;
		}{
			this.elements = new Object[size];
		}
	}

	public void add(T t) {
		// 先检查数组容量
		checkCapacity(size + 1);
		this.elements[size++] = t;
	}

	public void remove(int index) throws Exception{
		if (index < 0 || index >= this.elements.length){
			throw new Exception("xxxx");
		}
		int afterlen = this.elements.length - index - 1;
		System.arraycopy(this.elements, index + 1, this.elements, index, afterlen);
		this.elements[--size] = null;
	}

	public void checkCapacity(int i){
		int newCapacity = 0;
		if(this.elements == eles) {
			newCapacity = DEFALUT_CAPACITY;
		}
		if (i < this.elements.length - 1) {
			return;
		}else {
			if (newCapacity != 0) {
				this.elements = new Object[newCapacity];
			}else {
				// 重新计算容量
				int oldCapacity = this.elements.length;
				newCapacity = oldCapacity + (oldCapacity >> 1);

				Object[] newArr = new Object[newCapacity];
				System.arraycopy(this.elements, 0, newArr, 0, this.elements.length);
				this.elements = newArr;
			}
		}

	}
	public static void main(String[] args) {

		ArrayList r = new  ArrayList();
	}
}
```



### 5.String/正则表达式

### 6.IO流（序列化/反序列化）

### 7.面对对象特征（封装，继承，多态）

### 8.三层结构（代码开发结构）

### 9.连接数据库

### 10.mybatis + spring + spring mvc

view表示层 spring mvc

service业务数据层 spring

dao数据链路层 mybatis

### 11.spring 工作原理

### 12.spring boot

### 13.工程代码分块 svn git

### 14.多线程

```java
public class MyThread extends Thread{
    
}
class MyRunnable implements Runnable{
    
}
```

Thread和Runnable不同：

- 

syschronized锁方法锁的是每个当前对象得方法

syschronized锁代码块锁得是某个实例对象



![image-20200924141606150](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200924141606150.png)



![image-20200924141424617](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200924141424617.png)



### 15.购物模块

### 16.java 工作流程