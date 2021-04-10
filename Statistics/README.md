# Python统计分析

> 在这个项目中你将学习常用的python基本统计模块——pandas和matplotlib

文件`asmData.txt` 是3 个知名软件反汇编数据（基于Mac 平台，芯片非Mac M1），可以理解为是这些软件最终执行的计算机指令（机器指令是二进制编码，汇编语言与之一一对应并用助记符命名，以便于使用）。高级语言（C/C++、Python、Java 等）都要翻译成这种指令的集合。数据有多列，列与列之间用\t【Tab】间隔。第1-3 列数据可以忽略【第2、3 列数据也其实很重要】，第4 列是指令名称，其后两列是指令的参数【可以简单地将指令名称理解为函数，其后为其参数】。
特别提示：如数据不符合下图规范，可省略该行数据，不影响总体结论。

![image-20210410171532935](D:\cs50\Statistics\README.assets\image-20210410171532935.png)

## Task 1

统计每种指令使用频次，即统计每种指令出现次数，并放入到名为`Instruction.xlsx` 的Excel 文件中一个名为`instructionCount` 的sheet 中。第一列为Instruction，第二列为Count。

## Task 2

 统计每种指令的类别，即无参指令，单参指令，双参指令，多参指令。无参指令指指令后没有其他参数，单参指令指仅有一个参数，以此类推。将数据放到名为`Instruction.xlsx` 的Excel 文件中一个名为`instructionType` 的sheet 中。

## Task 3

在`Instruction.xlsx` 文件中增加一个名为Summary 的sheet，有三列数据，第一列是指令名称(Instruction)、频次(Amount)、类别（Type）【每个指令的类别，可能用到`vlookup`函数】。按频次从高低排序。

## Task 4

在`Instruction.xlsx` 文件中形成柱状图，并放入到一个名为Chart 的sheet 中。可能要用到数据透视表，计算出每种类别的指令数量。