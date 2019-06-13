# ChineseMaskReflector

**CMR — 使用掩码生成自定义中文用户名拼音爆破字典**

![Python 2.7 & 3.4](https://img.shields.io/badge/python-2.7&3.4-brightgreen.svg)



### 下载

```bash
git clone --depth=1 --branch=master https://github.com/LandGrey/ChineseMaskReflector.git
cd ChineseMaskReflector/
pip install requirements.txt
chmod +x cmr.py
python cmr.py -h
```



### 用法

```
                  ___  __  __  ____
                 / __)(  \/  )(  _ \
                ( (__  )    (  )   /
                 \___)(_/\/\_)(_)\_)        CMR v0.1

usage: cmr.py [-h] [-i INPUT] [-p PATTERN] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input chinese names file path, default: top-500
                        -chinese-name.txt
  -p PATTERN, --pattern PATTERN
                        chinese pinyin generation pattern, default:
                        {::}{::},{::}{::}{::}
  -o OUTPUT, --output OUTPUT
                        output path
```



### 概念

```
1. 一个中文姓名大多数以两位或者三位汉字组成，如:"孙大圣"，转成拼音为"sundasheng";
2. 一个汉字的拼音为一个占位符，一个占位符表示为 {位置:操作:范围/增加字符}；
3. 位置表示汉字的原始位置，如"1"表示"孙"，"2"表示"大"，"3"表示"圣";
4. 支持的操作有:
	字符全部小写: 'lower'	 (默认)
	字符全部大写: 'upper'
	字符逆序输出: 'reverse'
	在此增加字符: 'append'
	移除此字符 : 'remove'
5. "孙大圣"如果想要使用 cmr.py 生成姓名全拼，则可以使用的两种掩码表示形式如下:
表示一  {default:default:default}{default:default:default}{default:default:default}
表示二  {1:lower:>=1}{2:lower:>=1}{3:lower:>=1}
6. 其含义为生成的全拼第一位取原来的第一个汉字"孙"的拼音"sun"，同时字符格式为小写，并且保留"sun"的第一位及以后的所有字符，也就是三个字符都保留;第二位和第三位汉字的拼音同理。
7. 为了方便，以上两种形式的掩码可缩写为以下形式:
{::}{::}{::} 或 {1::}{2::}{3::} 等等
8. 两个汉字的姓名同理,掩码可缩写成 {::}{::} 或 {1::}{2::}
```



### 示例

```markdown
以下举例以"孙大圣"生成"sundasheng"形式的姓名拼音字典为标准形式, top-500-chinese-name.txt 替换为实际存在的中文姓名列表路径:

1. 直接生成中文姓名全拼字典 (sundasheng)
# 用逗号来分隔两位汉字和三位汉字组成的姓名拼音掩码
python cmr.py -i top-500-chinese-name.txt -p "{::}{::},{::}{::}{::}"


2. 姓名顺序颠倒 (dashengsun)
python cmr.py -i top-500-chinese-name.txt -p "{2::}{1::},{2::}{3::}{1::}"


3. 姓名顺序颠倒后名字只取第一个字符 (dssun)
python cmr.py -i top-500-chinese-name.txt -p "{2::=1}{1::},{2::=1}{3::=1}{1::}"


4. 只取每个汉字拼音首字符 (sds)
python cmr.py -i top-500-chinese-name.txt -p "{1::==1}{2::=1},{1::=1}{2::=1}{3::==1}"


5. 直接生成中文姓名全拼字典，但后面追加"@landgrey.me" 字符串 (sds@landgrey.me)
python cmr.py -i top-500-chinese-name.txt -p "{1::}{2::}{:append:@landgrey.me},{1::}{2::}{3::}{:append:@landgrey.me}"


6. 生成中文姓名全拼字典，但是姓只保留第一个字符且大写，和名字拼音中间用"@"隔开 (S@dasheng)
python cmr.py -i top-500-chinese-name.txt -p "{1:upper:=1}{:append:@}{2::},{1:upper:=1}{:append:@}{2::}{3::}"
```



### 其它

想对生成的姓名字典进一步处理，你可能需要 [**pydictor**](https://github.com/LandGrey/pydictor)

