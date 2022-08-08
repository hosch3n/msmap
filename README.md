# MSMAP

Msmap is a Memory WebShell Generator. Compatible with various Containers, Components, Encoder, *WebShell / Proxy / Killer* and Management Clients.

[简体中文](README_CN.md)

![](img/a.png)

<details>
<summary>Feature [WIP]</summary>

### Function

- [x] Dynamic Menu
- [x] Automatic Compilation
- [x] Generate Script
- [ ] Lite Mode
- [ ] Graphical Interface

### Container

- Java
  - [ ] Tomcat7
  - [x] Tomcat8
  - [x] Tomcat9
  - [x] Tomcat10
  - [ ] Resin
  - [ ] Weblogic
- .NET
  - [ ] IIS

### WebShell / Proxy / Killer

- WebShell
  - [x] CMD / SH
  - [x] AntSword
  - [x] JSPJS
  - [ ] Behinder
  - [ ] Godzilla
- Proxy
  - [ ] Neo-reGeorg
  - [ ] wsproxy
- Killer(As-Exploits)
  - [x] java-memshell-scanner
  - [x] ASP.NET-Memshell-Scanner

### Decoder / Decryptor / Hasher

- Decoder
  - [x] Base64
  - [ ] Hex
- Decryptor
  - [x] RC4
  - [x] AES128
  - [x] AES256
  - [ ] RSA
- Hasher
  - [x] MD5
  - [x] SHA128
  - [x] SHA256

</details>

## Usage

``` bash
git clone git@github.com:hosch3n/msmap.git
cd msmap
python generator.py
```

> [Warning] MUST set a unique password, Options are case sensitive.

### Advanced

Edit `config/environment.py`

``` python
# Auto Compile
auto_build = True

# Base64 Encode Class File
b64_class = True

# Generate Script File
generate_script = True

# Compiler Absolute Path
java_compiler_path = r"~/jdk1.6.0_04/bin/javac"
dotnet_compiler_path = r"C:\Windows\Microsoft.NET\Framework\v2.0.50727\csc.exe"
```

Edit `gist/java/container/tomcat/servlet.py`

``` java
// Servlet Path Pattern
private static String pattern = "*.xml";
```

WsFilter暂不支持自动编译。如果使用了加密编码器，密码需要与路径相同（如`/passwd`）

## Example

<details>
<summary>CMD / SH</summary>

**Command** with **Base64** Encoder | Inject Tomcat Valve

`python generator.py Java Tomcat Valve Base64 CMD passwd`

</details>

<details>
<summary>AntSword</summary>

Type **JSP** with **default** Encoder | Inject Tomcat Valve

`python generator.py Java Tomcat Valve RAW AntSword passwd`

Type **JSP** with **[aes_128_ecb_pkcs7_padding_md5](extend/AntSword/encoder/aes_128_ecb_pkcs7_padding_md5.js)** Encoder | Inject Tomcat Listener

`python generator.py Java Tomcat Listener AES128 AntSword passwd`

Type **JSP** with **[rc_4_sha256](extend/AntSword/encoder/rc_4_sha256.js)** Encoder | Inject Tomcat Servlet

`python generator.py Java Tomcat Servlet RC4 AntSword passwd`

</details>

## Reference

[GodzillaMemoryShellProject](https://github.com/BeichenDream/GodzillaMemoryShellProject)

[AntSword-JSP-Template](https://github.com/AntSwordProject/AntSword-JSP-Template)

[As-Exploits memshell_manage](https://github.com/yzddmr6/As-Exploits/tree/master/core/memshell_manage)

[Behinder](https://github.com/rebeyond/Behinder) | [wsMemShell](https://github.com/veo/wsMemShell) | [ysomap](https://github.com/wh1t3p1g/ysomap)