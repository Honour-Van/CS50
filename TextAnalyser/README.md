# 文本分析器
## 文本选取
课程选择了三国演义，属于小说，约64w字。

这里我们选择讲稿和长文两种类型，作为体裁的区分，同时熟悉GB级文本分析。

## 讲稿分析
https://blog.csdn.net/weixin_45502929/article/details/106363436

处理得到文本之后，直接输入
```sh
Building prefix dict from the default dictionary ...
Dumping model to file cache C:\Users\abc44\AppData\Local\Temp\jieba.cache
Loading model cost 1.403 seconds.
Prefix dict has been built successfully.
经统计，共有12078个不同的词
您想查看前多少个人物？[10]:  
1. 我们 2290
2. 中国 1472
3. 这个 1040
4. 一个 877
5. 所以 858
6. 社会主义     591
7. 社会 543
8. 发展 516
9. 就是 483
10. 一些        461
已写入文件：./output.csv
```

观察csv，定义ignore list
```python
ignore_list =  ['我们', '这个', '一个', '所以', 
                '就是', '一些', '大家', '那么', 
                '可能', '什么', '非常', '这种',
                '就是说']
```

完成词云
![词云1](./wordcloud1.png)

下一步重点在从中提取更有价值的东西，比如较长的词可能会包含更多的东西？二字口语意义鲜少？


