# Web开发练习

目标效果如图所示。图片第一行显示成绩的排序方式，即按姓
名、平时成绩、期中成绩、期末成绩、总成绩中的某一项升序或降
序排列；单击提交按钮，则按指定的方式排序成绩；

![image-20210410165541459](D:\cs50\Web\README.assets\image-20210410165541459.png)



### 说明

总成绩的计算方式是：平时成绩和期中成绩占30%，期末成绩占
40%，四舍五入。Python 提供round()函数，具体用法查找相关资
料。

成绩表格采用HTML 表格实现。该表格的部分代码如下：

```html
<table cellpadding='0' cellspacing='0' border='1'>
<tr><th>姓名</th><th>平时成绩</th><th>期中成绩</th><th>期末成绩
</th><th>总成绩</th><th>可视</th></tr>
<tr><td>陈子昂
</td><td>97</td><td>100</td><td>94</td><td>97</td><td><div
class='stateDiv' style='backgroundcolor:
Green;width:97px;'></div></td></tr>
</table>
```

 “可视”列中颜色的宽度与分数相关，大于等于85 为绿色Green，大
于等于60 小于85 为黄色Yellow，其余为红色Red；

在head-style 中定义th、td 和stateDiv 的style 内容，使其效果尽量与图片一致，不要求绝对一致；

相关数据在附件中(poetScore.txt)，不得用其他源数据；

附加要求：可分别实现两个版本，即排序在Python+Flask 端完成，
或者在浏览器端的网页部分完成。另外，思考如果有分数录入模
块，分数查看模块，浏览器端排序是否会导致数据不一致，如何规
避？

### 代码实现
#### 数据组织
在python文件中利用二维列表读入名称并计算，并排序。

本来尝试用json组织数据
```python
def txt2json():
    with open("poetScore.txt", 'r', encoding='utf-8') as f:
        f.readline()
        data = ""
        for line in f.readlines():
            content = line.split(',')
            score = round((int(content[1])+int(content[2])+int(content[3]))/3)
            data = data + \
                f'{{"name":"{content[0]}","usual":{content[1]},"midterm":{content[2]},"final":{content[3]},"score":{score}}},'
        data = data[:-1]
    with open("poetScore.json", 'w', encoding='utf-8') as f:
        f.write(data)   
```
但是由于数据中的重复，所以我们不采用这个方法。显然作为一个排名，其中可能存在重名。
```python
with open('poetScore.txt', 'r', encoding='utf-8') as f:
    df1 = pd.DataFrame(pd.read_csv('poetScore.txt'))
```

dataFrame添加列：**https://blog.csdn.net/zx1245773445/article/details/99445332**</br>
行的遍历：**https://blog.csdn.net/ls13552912394/article/details/79349809**


#### Flask render_template

#### 动态部分的构建
dataframe排序：**https://blog.csdn.net/houyanhua1/article/details/87804111**

排序之后，利用Python生成HTML表格代码

#### 网页radio获取
https://blog.csdn.net/newborn2012/article/details/17289345

flask和html中js脚本的交互，注意，网址虽然是大小写不敏感的，但是在写接口的时候是敏感的。


#### 拼音排名
使用xpinyin模块

dataframe列改名

### 补充内容
尝试将df传到前端进行处理

#### 将json对象传递到前端
**https://www.cnblogs.com/lazyboy1/p/5015111.html**

采用了其中的方法5，但是模板中的替代数据是字符串即可。

然后是排序，**https://www.jianshu.com/p/92c3bf42a7b1**

排序在点击按钮的时候扫描得出模式，然后进行排序。

![image-20210416223018697](D:\cs50\Web\README.assets\image-20210416223018697.png)

预估是table的html代码发生了问题。观察如下：

![image-20210416233457791](D:\cs50\Web\README.assets\image-20210416233457791.png)

查找资料，我们发现这是因为jquery会自动生成tbody，将加入的tr直接加入进去。这时候如果按照如下代码分次加入，则会使得空的tr被提取到tbody中。

```javascript
$.each(data, function (index, value) {
    $("table").append("<tr id='rd'>");
    $("table").append(`<td>${value.name}</td>`);
    $("table").append(`<td>${value.平时成绩}</td>`);
    $("table").append(`<td>${value.期中成绩}</td>`);
    $("table").append(`<td>${value.期末成绩}</td>`);
    $("table").append(`<td>${value.总成绩}</td>`);
    if (basis !== "姓名") {
        var vis = value[basis];
        var color = choose_color(vis);
        $("table").append(`<td><div class='stateDiv' style='background:${color}; width:${vis}px;'></div></td></tr>`);
    }
    $("table").append('</tr>');
});
```

因而我们可以通过一次性添加的方式来解决这个问题：

```javascript
$.each(data, function (index, value) {
    rowdata = `<tr id='rd'><td>${value.name}</td><td>${value.平时成绩}</td><td>${value.期中成绩}</td><td>${value.期末成绩}</td><td>${value.总成绩}</td>`
    if (basis !== "姓名") {
        var vis = value[basis];
        var color = choose_color(vis);
        rowdata += `<td><div class='stateDiv' style='background:${color}; width:${vis}px;'></div></td></tr>`;
    }
    rowdata += '</tr>';
    $("table").append(rowdata);
});
```

问题显然已经得到了解决：

![image-20210416234624147](D:\cs50\Web\README.assets\image-20210416234624147.png)



当然我们也可以自己编写tbody来避免这个问题。这篇博客https://blog.csdn.net/wangdabin_1216/article/details/8206043给出的方法是写全tbody，减小不确定性。

```javascript
function add(udata){$("table tbody").append(udata);}
add("<tr id='rd'>");
add(`<td>${value.name}</td>`);
add(`<td>${value.平时成绩}</td>`);
add(`<td>${value.期中成绩}</td>`);
add(`<td>${value.期末成绩}</td>`);
add(`<td>${value.总成绩}</td>`);
if (basis !== "姓名") {
    var vis = value[basis];
    var color = choose_color(vis);
    add(`<td><div class='stateDiv' style='background:${color}; width:${vis}px;'></div></td></tr>`);
}
add('</tr>');

```

为了避免更多次修改source代码，这种方法不一定是更好的，但不犯懒，去定义tbody一定是没错的。