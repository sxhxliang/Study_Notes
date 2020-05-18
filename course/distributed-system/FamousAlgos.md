# 一些很著名的算法

## Elastic Search

### 核心术语
下面介绍Lucene中的核心术语。
- Term：是索引里最小的存储和查询单元，对于英文来说一般是指一个单词，对于中文来说一般是指一个分词后的词。
- 词典（Term Dictionary，也叫作字典）：是Term的集合。词典的数据结构可以有很多种，每种都有自己的优缺点，比如：排序数组通过二分查找来检索数据：HashMap（哈希表）比排序数组的检索速度更快，但是会浪费存储空间；fst(finite-state transducer)有更高的数据压缩率和查询效率，因为词典是常驻内存的，而fst有很好的压缩率，所以fst在Lucene的最新版本中有非常多的使用场景，也是默认的词典数据结构。
- 倒排序（Posting List）：一篇文章通常由多个词组成，倒排表记录的是某个词在哪些文章中出现过。
- 正向信息：原始的文档信息，可以用来做排序、聚合、展示等。
- 段（segment）：索引中最小的独立存储单元。一个索引文件由一个或者多个段组成。在Luence中的段有不变性，也就是说段一旦生成，在其上只能有读操作，不能有写操作。

### ES中的文档相似度排序
[相关度评分背后的理论-官网](https://www.elastic.co/guide/cn/elasticsearch/guide/cn/scoring-theory.html)

Lucene（或 Elasticsearch）使用 **布尔模型**（Boolean model）查找匹配文档，并用一个名为实用评分函数的公式来计算相关度。这个公式借鉴了 **词频/逆向文档频率**（term frequency/inverse document frequency） 和 **向量空间模型**（vector space model），同时也加入了一些现代的新特性，如协调因子（coordination factor），字段长度归一化（field length normalization），以及词或查询语句权重提升。

#### 布尔模型
倒排索引
布尔模型（Boolean Model） 只是在查询中使用 AND 、 OR 和 NOT （与、或和非）这样的条件来查找匹配的文档，以下查询：
```
full AND text AND search AND (elasticsearch OR lucene)
```
会将所有包括词 full 、 text 和 search ，以及 elasticsearch 或 lucene 的文档作为结果集。这个过程简单且快速，它将所有可能不匹配的文档排除在外。

#### BM25
BM25（Best Matching）函数同样使用词频与逆文档频率衡量一个Term的重要程度，其与TF/IDF算法主要存在两个区别：
- 非线性文档饱和度：term-frequency 通过一个调节因子`k1`控制饱和速度，出现频率达到一定阈值则`tf()`会趋于饱和。
- 字段长度归一化： Lucene 认为长文章会自然而然的导致高tf，因此需要进行归一化削弱这一作用。

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/43e5c609557364f7836b6b2f4cd8ea41deb86a96)

其中`f(q_i, D)`为词频，`|D|`为文档长度， `avgdl`为平均文档长度。
