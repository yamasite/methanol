#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Developed by Lutkin Wang
# Check prototype in code blocks such as:
#  <codeblock props="android" outputclass="language-java">
#  public abstract int addVideoWatermark(String watermarkUrl, WatermarkOptions options);
#  </codeblock>

import os
import re

# Code location
code_location = "C:\\Users\\WL\\Documents\\rte_sdk\\proj.android\\src\\main\\java\\io"
# DITA location
dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\API"

decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"

# A list of DITA files
dita_file_list = []

# A list of DITA protos
dita_proto_list = []

# A list of code files
code_file_list = []

# A list of proto files
code_proto_list = []


def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string


def write_log(text):
    with open("log_android.txt", encoding='utf8', mode='a') as f:
        f.write(text + "\n")


# Handle the DITA files
for file in os.scandir(dita_location):
    if (file.path.endswith(".dita")) and not file.path.startswith(dita_location + "\enum_") and file.is_file():
        print(file.path)
        dita_file_list.append(file.path)
        with open(file.path, encoding='utf8') as f:
            content = f.read()
            # Use substring methods to get the proto from DITA
            after_codeblock_start_tag = re.split('<codeblock props="android" outputclass="language-java">', content)
            try:
                before_codeblock_end_tag = re.split('</codeblock>', after_codeblock_start_tag[1])
            except IndexError:
                proto_text = "Error: No prototype"
            proto_text = before_codeblock_end_tag[0]
            print(proto_text)

            dita_proto_list.append(proto_text)

dictionary = dict(zip(dita_file_list, dita_proto_list))

# Handle the interface files

# Decomment all java files
for root, dirs, files in os.walk(code_location):
    for file in files:
        if file.endswith(".java"):
            with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                text = removeComments(f.read())
                with open(decomment_code_location + "/" + "concatenated.java", encoding='utf8', mode='a') as f1:
                    f1.write(text)

with open(decomment_code_location + "/" + "concatenated.java", encoding='utf8', mode='r') as f:
    content = f.read()
    content1 = content.replace("&amp;", "&")
    content2 = content1.replace("&lt;", "<")
    content3 = content2.replace("&gt;", ">")
    content4 = content3.replace(" ", "")
    content5 = content4.replace("\n", "")

    open("log_android.txt", "w").close()

    i = 1

    for file, code in dictionary.items():
        code1 = code.replace("&amp;", "&")
        code2 = code1.replace("&lt;", "<")
        code3 = code2.replace("&gt;", ">")
        code4 = code3.replace(" ", "")
        code5 = code4.replace("\n", "")

        if content5.find(code5) == -1:
            write_log("No. " + str(i) + " Mismatch found")
            i = i + 1
            write_log("\n")
            write_log("-------------------------------------------------------------------------------")
            write_log("-------------------------------------------------------------------------------")
            write_log("For the DITA file: " + file)
            write_log("This prototype in DITA cannot be located in the source code: \n " + code + "\n")
            write_log("-------------------------------------------------------------------------------")
            write_log("-------------------------------------------------------------------------------")
            write_log("\n")
