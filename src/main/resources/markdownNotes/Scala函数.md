## Scala函数：

### Java Lambda表达式:

#### 函数式接口:

- 一种只含有一个抽象方法声明的接口
- 可以使用匿名内部类来实例化函数式接口的对象
- 通过lambda表达式进一步简化代码

#### 内置四大函数式接口

- 消费接口：Consumer<T>
- 供给型接口：
- 断言型接口
- 函数型接口

java

```java
new Thread(() -> System.out.println("hello")).start();
```

scala

```js
 new Thread(_ => print("11")).start()
```

