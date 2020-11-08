## LRU缓存机制

> 运用你所掌握的数据结构，设计和实现一个  LRU (最近最少使用) 缓存机制。它应该支持以下操作： 获取数据 get 和 写入数据 put 。

> 获取数据 get(key) - 如果关键字 (key) 存在于缓存中，则获取关键字的值（总是正数），否则返回 -1。
> 写入数据 put(key, value) - 如果关键字已经存在，则变更其数据值；如果关键字不存在，则插入该组「关键字/值」。当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。

`示例` 

```java
LRUCache cache = new LRUCache( 2 /* 缓存容量 */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // 返回  1
cache.put(3, 3);    // 该操作会使得关键字 2 作废
cache.get(2);       // 返回 -1 (未找到)
cache.put(4, 4);    // 该操作会使得关键字 1 作废
cache.get(1);       // 返回 -1 (未找到)
cache.get(3);       // 返回  3
cache.get(4);       // 返回  4
```

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lru-cache



### LinkedHashMap解法：

继承LinkedHashMap，LHM底层的访问顺序的维护机制是和LRU几乎一模一样，所以直接拿来用即可。

- `void afterNodeAccess(Node<K,V> p) { }`

  > 其作用就是在访问元素之后，将该元素放到双向链表的尾巴处(所以这个函数只有在按照读取的顺序的时候才会执行)

- `void afterNodeRemoval(Node<K,V> p) { }`

  > 其作用就是在删除元素之后，将元素从双向链表中删除.

- `void afterNodeInsertion(boolean evict) { }`

  > 这个才是我们题目中会用到的，在插入新元素之后，需要回调函数判断是否需要移除一直不用的某些元素！



#### JAVA版：

```java
class LRUCache extends LinkedHashMap<Integer, Integer>{
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75F, true);
        this.capacity = capacity;
    }

    public int get(int key) {
        return super.getOrDefault(key, -1);
    }

    // 这个可不写
    public void put(int key, int value) {
        super.put(key, value);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity; 
    }
}
```

#### scala版：

```js
class LRU(_capacity: Int) extends util.LinkedHashMap[Integer, Integer](_capacity, 0.75F, true) {

  def get(key: Int): Int = super.getOrDefault(key, -1)

  // 这个可不写
  def put(key: Int, value: Int): Unit = super.put(key, value)

  override protected def removeEldestEntry(eldest: util.Map.Entry[Integer, Integer]): Boolean = size > _capacity

}
```

具体的LinkedHashMap是如何实现的：

>https://www.jianshu.com/p/8f4f58b4b8ab