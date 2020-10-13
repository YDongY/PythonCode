# Pytest Tutorial

![](https://docs.pytest.org/en/stable/_static/pytest1.png)

> 官方文档：[https://docs.pytest.org/en/stable/contents.html](https://docs.pytest.org/en/stable/contents.html)
>
> 本书源代码下载：[https://pragprog.com/titles/bopytest/python-testing-with-pytest/](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)

## 安装

```shell script
pip install pytest
```

## 快速上手

- 新建一个测试文件 test_success.py

```python
def test_passing():
    assert (1, 2, 3) == (1, 2, 3)
```

```shell script
$ pytest test_success.py
================================================= test session starts =================================================
platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/ydongy/Code/code_snippets/Pytest_Tutorial
collected 1 item                                                                                                      

test_success.py .                                                                                               [100%]

================================================== 1 passed in 0.00s ==================================================                                                                                             [100%]
```

`test_success.py .` 后面的 `.` 表示当前文件中的测试用例全部通过，如果觉得不太明显可以添加一个 `-v` 参数

```shell script
$ pytest -v test_success.py
================================================= test session starts =================================================
platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1 -- /home/ydongy/.local/share/virtualenvs/pytest/bin/python
cachedir: .pytest_cache
rootdir: /home/ydongy/Code/code_snippets/Pytest_Tutorial
collected 1 item                                                                                                      

test_success.py::test_passing PASSED                                                                            [100%]

================================================== 1 passed in 0.00s ==================================================
```

`test_success.py::test_passing PASSED`　可以看到当前文件的 test_passing 测试用例 PASSED 通过


- 新建一个错误测试文件 test_fail.py

```python
def test_fail():
    assert (1, 2, 3) == (3, 2, 3)
```

```shell script
$ pytest -v test_fail.py   
================================================================================= test session starts ==================================================================================
platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1 -- /home/ydongy/.local/share/virtualenvs/pytest/bin/python
cachedir: .pytest_cache
rootdir: /home/ydongy/Code/code_snippets/Pytest_Tutorial
collected 1 item                                                                                                                                                                       

test_fail.py::test_fail FAILED                                                                                                                                                [100%]

======================================================================================= FAILURES =======================================================================================
_____________________________________________________________________________________ test_passing _____________________________________________________________________________________

    def test_fail():
>       assert (1, 2, 3) == (3, 2, 3)
E       assert (1, 2, 3) == (3, 2, 3)
E         At index 0 diff: 1 != 3
E         Full diff:
E         - (3, 2, 3)
E         ?  ^
E         + (1, 2, 3)
E         ?  ^

test_fail.py:6: AssertionError
=============================================================================== short test summary info ================================================================================
FAILED test_fail.py::test_fail - assert (1, 2, 3) == (3, 2, 3)
================================================================================== 1 failed in 0.02s ===================================================================================
```

通过 `-v` 参数测试一个错误的测试用例，可以的到详细的错误位置信息，`^` 表示错误位置

**可以注意到我们的两个测试文件都是 test_xxx.py，其好处是当我们直接执行 pytest 的时候，会自动查找当前目录及其子目录的所有 `test_` 开头的文件并且执行其文件中　test 开头的函数，当然还有通过类的方式也会一起测试**

即测试命名规则如下：

- 测试文件命名：`test_<something>.py` 或者 `<something>_test.py`
- 测试函数和测试类方法：`test_<something>.py`
- 测试类：`Test<something>`

### 输出信息详解

```shell script
$ pytest test_success.py
================================================= test session starts =================================================
platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/ydongy/Code/code_snippets/Pytest_Tutorial
collected 1 item                                                                                                      

test_success.py .                                                                                               [100%]

================================================== 1 passed in 0.00s ==================================================
```

- `test session starts`：pytest 会为每个测试回话做明确分割，一段会话就是 pytest 的一次调用
- `platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1`：一些环境和依赖以及版本
- `rootdir: /home/ydongy/Code/code_snippets/Pytest_Tutorial`：当前文件所在的根目录，也是 pytest 进行搜索测试代码的目录
- `collected 1 item  `：搜索范围内找到的测试条目数量，
- `test_success.py . `：表示测试文件，`.(PASSED)`表示通过，Failure(失败)，error(异常)，skip(跳过)，xfail(预期失败)，xpass(预期失败并通过)，会分别标记为 F,E,s,x,X
- `1 passed in 0.00s`：表示测试通过数量以及这段会话耗费的时间

**测试类型**

- `PASSED(.)`：测试通过
- `FAILED(F)`：测试失败
- `SKIPPED(.)`：测试未执行，可以将测试标记为 `@pytest.mark.skip()`或者`@pytest.mark.skipif()`
- `xfail(x)`：预期失败，并且确实失败　使用`@pytest.mark.xfail()`

```python
import pytest

@pytest.mark.xfail()
def test_fail():
    assert (1, 2, 3) == (3, 2, 3)

```
- `XPASS(X)`：预期失败，实际通过
- `ERROR(E)`：测试之外的代码异常

### 运行单个测试用例

格式：`pytest -v xxx/test_xxx.py::test_xxx

```shell script
pytest ./test_fail.py::test_fail
```

### pytest 常用参数

- `--collection-only`：查看运行的测试用例
- `-k`：允许使用表达式指定希望运行的测试用例

```shell
pytest -k "fail or success"

# 表示希望运行`test_fail.py`和`test_success.py`
```

- `-m`：用来标记测试并分组，比如`test_fai()`和`test_success()`不在同一个文件想要同时测试，可以使用`@pytest.mark.xxx`，xxx 是标记名可以随便取，比如`@pytest.mark.run_success_fail`，最终运行命令

```shell
pytest -k run_success_fail
```

也可以使用表达式指定多个标记`-m "xxx and yyy"` 或者 `-m "xxx not and yyy"`

- `-x`：表示遇到断言失败就中断整个测试
- `-maxfail=num`：表示断言失败几次后中断，`-maxfail=1` 和 `-x` 是同样的效果
- `-s`：允许终端测试运行时输出其某些结果
- `--lf`：当出现多个测试失败，通过该参数可以快速定位到最后一个失败用例并重新运行，最好加上`--tb`使用
- `--ff`：与`--lf`作用基本相同，只不过会运行完剩余的测试用例
- `-v`：详细信息
- `-q`：简单信息
- `--duration=N`：统计测试过程那几个阶段（包括 call，setup，teardown）最慢

## 编写测试用例

### 预期异常

```python
import pytest

def test_xxx():
    with pytest.raises(TypeError):
        # ......
        pass
```

当 with 语句块中的测试通过，说明抛出　TypeError 异常。如果抛出的是其他类型的异常，表示与我们预期的不一致，说明测试失败

### 测试标记

pytest 提供了标记机制，允许使用　marker 对测试函数进行标记，一个函数可以有多个

```python
import pytest

@pytest.mark.zzz
@pytest.mark.yyy
def test_xxx():
    pass
```

```shell script
pytest -v -m "zzz and yyy" xxx.py
pytest -v -m "zzz not and yyy" xxx.py
```

### 跳过测试

```python
import pytest

@pytest.mark.skip(reason="跳过测试的理由")
def test_xxx():
    pass
```

### 标记预期失败

```python
import pytest

@pytest.mark.xfail()
def test_xxx():
    pass
```

### 单个目录测试

```shell script
pytest xxx/yyy --tb=no
```

### 单个文件

```shell script
pytest xxx/yyy/zzz.py
```


### 单个测试函数

```shell script
pytest -v xxx/yyy/zzz.py::test_xxx
```

### 单个测试类

```shell script
pytest -v xxx/yyy/zzz.py::TestXxx
```

### 单个测试类中测试方法

```shell script
pytest -v xxx/yyy/zzz.py::TestXxx::test_xxx
```

### 参数化测试

```python
import pytest

@pytest.mark.parametrize(argnames="x,y,z",argvalues=[(1,2,3),(4,5,6)])
def test_xxx(x,y,z):
    pass

# argnames:参数
# argvalues：参数对应值的列表
```

## Pytest Fixture

fixture 是在测试函数运行前后，由 pytest 执行的外壳函数

- 声明函数是一个 fixture

```python
import pytest

@pytest.fixture()
def some_data():
    return 42

def test_some_data(some_data):
    assert some_data==42
```

- 使用 fixture 连接和断开数据库

```python
import pytest

@pytest.fixture()
def tasks_db():
    # Setup : start db
    yield 
    # Teardown : stop db
```

fixture 函数会在测试函数之前运行，但是如果 fixture 函数包含 yield 那么系统会在 yield 停止，转而运行测试函数，等到测试函数执行完成再回到 fixture ，继续执行 yield 后面的代码。无论测试过程发生什么，yield 之后的代码都会执行

可以通过 `--setup-show` 来查看测试过程，其中包含 fixture 函数

```shell script
$ pytest --setup-show test_xxx.py

SETUP ...
    ...
    ...
TEARDOWN ...
```


### 使用　fixture 传递参数

```python
import pytest

@pytest.fixture()
def a_tuple():
    return (1,'foo',None,{'bar':23})

def test_a_tuple(a_tuple):
    assert a_tuple[3]['bar']==32
```

### 使用多个 fixture

```python

```


### 指定 fixture 作用范围

fixture 包含 scope 的参数，有四个待选值：

- function（默认）：函数级别的 fixture 每个测试函数只运行一次，在测试函数运行之前和之后运行
- class：类级别的 fixture 每个测试类只需要运行一次，无论测试类有多少类方法都可以共享
- module：模块级别的 fixture 每个模块只需要运行一次
- session：会话级别 fixture 每次会话只需要运行一次


```python
import pytest

@pytest.fixture(scope='function')
def func_scope():
    pass

@pytest.fixture(scope='class')
def class_scope():
    pass

@pytest.fixture(scope='module')
def mod_scope():
    pass

@pytest.fixture(scope='session')
def sess_scope():
    pass

def test_1(sess_scope,mod_scope,func_scope):
    pass

@pytest.mark.usefixtures('class_scope')
class TestSomething(object):
    def test_2(self):
        pass
    def test_3(self):
        pass
```

### fixture 重命名

```python
import pytest

@pytest.fixture(name="aaa")
def xxx():
    pass

def test_xxx(aaa):
    pass
```

通过 `--fixture` 参数可以提供所测试文件名

```shell script
pytest --fixture xxx.py
```

### fixture 参数化

```python
import pytest

@pytest.fixture(params=[1,2,3])
def xxx(request):
    # request 属于内键 params
    return request.params

def test_xxx(xxx):
    pass
```

## 内置 Fixture
