###  javascript清空数组的三种方法:

- 长度清零

```javascript
arr.length = 0;
```



- splice函数

  **splice(index,howmany,element1,.....,elementX)**

  - index：必选，规定从何处添加/删除元素。

  - howmany：必选，规定应该删除多少元素。未规定此参数，则删除从 index 开始到原数组结尾的所有元素。

  - element1:可选，规定要添加到数组的新元素。

```javascript
arr.splice(0,arr.length);  
```



- 直接赋予新数组

```javascript
var arr = [1,2,3,4];  
arr = [];
```



