# 一些很著名的算法

## Elastic Search

### 核心术语
下面介绍Lucene中的核心术语。
- Term：是索引里最小的存储和查询单元，对于英文来说一般是指一个单词，对于中文来说一般是指一个分词后的词。
- 词典（Term Dictionary，也叫作字典）：是Term的集合。词典的数据结构可以有很多种，每种都有自己的优缺点，比如：排序数组通过二分查找来检索数据：HashMap（哈希表）比排序数组的检索速度更快，但是会浪费存储空间；fst(finite-state transducer)有更高的数据压缩率和查询效率，因为词典是常驻内存的，而fst有很好的压缩率，所以fst在Lucene的最新版本中有非常多的使用场景，也是默认的词典数据结构。
- 倒排序（Posting List）：一篇文章通常由多个词组成，倒排表记录的是某个词在哪些文章中出现过。
- 正向信息：原始的文档信息，可以用来做排序、聚合、展示等。
- 段（segment）：索引中最小的独立存储单元。一个索引文件由一个或者多个段组成。在Luence中的段有不变性，也就是说段一旦生成，在其上只能有读操作，不能有写操作。

### 1. ES中的文档相似度排序
[相关度评分背后的理论-官网](https://www.elastic.co/guide/cn/elasticsearch/guide/cn/scoring-theory.html)

Lucene（或 Elasticsearch）使用 **布尔模型**（Boolean model）查找匹配文档，并用一个名为实用评分函数的公式来计算相关度。这个公式借鉴了 **词频/逆向文档频率**（term frequency/inverse document frequency） 和 **向量空间模型**（vector space model），同时也加入了一些现代的新特性，如协调因子（coordination factor），字段长度归一化（field length normalization），以及词或查询语句权重提升。

#### 1.1 布尔模型
![](https://upload-images.jianshu.io/upload_images/8796251-ea214e89b36af291.png?imageMogr2/auto-orient/strip|imageView2/2/w/1160/format/webp)
ES会建立倒排索引存储某个Term出现过的文档编号，通过对两个链表取交集、并集、差集即可实现 AND，OR，NOT 操作。

布尔模型（Boolean Model） 只是在查询中使用 AND 、 OR 和 NOT （与、或和非）这样的条件来查找匹配的文档，以下查询：
```
full AND text AND search AND (elasticsearch OR lucene)
```
会将所有包括词 full 、 text 和 search ，以及 elasticsearch 或 lucene 的文档作为结果集。这个过程简单且快速，它将所有可能不匹配的文档排除在外。

#### 1.2 BM25
BM25（Best Matching）函数同样使用词频与逆文档频率衡量一个Term的重要程度，其与TF/IDF算法主要存在两个区别：
- 非线性文档饱和度：term-frequency 通过一个调节因子`k1`控制饱和速度，出现频率达到一定阈值则`tf()`会趋于饱和。
- 字段长度归一化： Lucene 认为长文章会自然而然的导致高tf，因此需要进行归一化削弱这一作用。

![](https://www.elastic.co/guide/cn/elasticsearch/guide/current/images/elas_1706.png)

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/43e5c609557364f7836b6b2f4cd8ea41deb86a96)

其中`f(q_i, D)`为词频，`|D|`为文档长度， `avgdl`为平均文档长度。

#### 1.3 向量空间模型
向量空间模型（vector space model） 提供一种比较多词查询的方式，单个评分代表文档与查询的匹配程度，为了做到这点，这个模型将文档和查询都以 向量（vectors） 的形式表示：

向量实际上就是包含多个数的一维数组，例如：
```
[1,2,5,22,3,8]
```

在向量空间模型里，向量空间模型里的每个数字都代表一个词的 权重 ，与 词频/逆向文档频率的计算方式类似。

设想如果查询 “happy hippopotamus” ，常见词 happy 的权重较低，不常见词 hippopotamus 权重较高，假设 happy 的权重是 2 ， hippopotamus 的权重是 5 ，可以将这个二维向量—— [2,5] ——在坐标系下作条直线，线的起点是 (0,0) 终点是 (2,5) ，如图 Figure 27, “表示 “happy hippopotamus” 的二维查询向量” 。

现在，设想我们有三个文档：

```
I am happy in summer 。
After Christmas I’m a hippopotamus 。
The happy hippopotamus helped Harry 。
```

可以为每个文档都创建包括每个查询词—— happy 和 hippopotamus ——权重的向量，然后将这些向量置入同一个坐标系中，如图 Figure 28, ““happy hippopotamus” 查询及文档向量” ：

```
文档 1： (happy,____________) —— [2,0]
文档 2： ( ___ ,hippopotamus) —— [0,5]
文档 3： (happy,hippopotamus) —— [2,5]
```
![](https://www.elastic.co/guide/cn/elasticsearch/guide/cn/images/elas_17in02.png)

向量之间可以测量query向量和文档向量之间的角度就可以得到每个文档的相关度，文档 1 与查询之间的角度最大，所以相关度低；文档 2 与查询间的角度较小，所以更相关；文档 3 与查询的角度正好吻合，完全匹配。

