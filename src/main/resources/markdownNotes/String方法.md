- **char charAt(int index)**：
  - 返回指定索引处的char值
- **int compareTo(Object o)**：
  - 把这个字符串和另一个对象比较
- **String concat(String str)**：
  - 指定字符串连接到此字符串的结尾
- **boolean endsWith(String suffix)**
  - 测试此字符串是否以指定的后缀结束
- **boolean equals(Object anObject)**
  - 将此字符串与指定对象比较
- **boolean equalsIgnoreCase(String anthoerString)**
  - 将此String与另一个String比较，不考虑大小写
- **byte[] getBytes()**
  - 打成byte序列，将结果存储到一个新的byte数组中
- **byte[] getBytes(String charseName)**
  - 指定字符集将此打成byte序列，将结果存储到一个新的byte数组中

- **int hashCode()**
  - 返回此字符串的哈希码
- **int indexOf(int ch)**
  - 返回指定数字字符在此字符串中第一次出现的索引
- **int indexOf(String str)**
  - 返回指定子字符串在此字符串中第一次出现的索引
- **String intern()**
  - 返回字符串对象的规范化表示形式
- **int lastIndexOf(int ch)**
  - 返回指定数字字符在此字符串中最后一次出现的索引
- **int lastIndexOf(String str)**
  - 返回指定子字符串在此字符串中最后一次出现的索引
- **int length()**
  - 返回字符串的长度
- **boolean matches(String regex)**
  - 告知此字符串是否匹配给定的正则表达式
- **String replace(char oldChar, char newChar)**----xx.replace
  - 返回新字符串，通过newChar替换此字符串中出现所有的oldChar
- **String replaceAll(String regex,  String replacement)**
  - 是用replacement去替换所有用正则匹配字符串成功的地方
- **String replaceFirst(String regex,  String replacement)**
  - 是用replacement去替换所有用正则匹配字符串成功的第一个地方
- **String[] split(String regex)**
  - 利用正则去拆分字符串
- **boolean startsWith(String prefix)**
  - 测试字符串是否以指定前缀开始
- **boolean startsWith(String prefix，int toffset)**
  - 测试是否以索引开始的字符串的指定前缀开始

- **String substring(int beginindex, int endindex)**

  - 返回新的指定的子串，通过开始和结尾的位置

- **char[] toCharArray()**

  - 将字符串转换为新的字符数组

- **String toLowerCase()**

  - String全部转成小写

- **String toUpperCase()**

  - String全部转成大写

- **String trim()**

  - 返回字符串副本，忽略前后空白

  

  

  