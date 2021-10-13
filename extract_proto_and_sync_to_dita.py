#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# Developed by Lutkin Wang
#
# Story: Based on the condition that we have a one-to-one mapping between APIs in each platform,
# extract and replenish prototypes based on CPP APIs.
#
# Step 1: Extract the CPP (benchmark) prototypes
# Step 2: Search (fuzzy search) for the corresponding prototype in the interface file of a certain SDK
# Step 3: Replenish the correct prototype
#

import os
import re


def main():

    # Code location
    code_location = "C:\\Users\\WL\\Documents\\rte_sdk\\interface\\cpp"
    # DITA location
    dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\API"

    # dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"

    decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"

    # A list of DITA files
    dita_file_list = []

    # A list of DITA protos
    dita_proto_list = []

    # A list of code files
    code_file_list = []

    # A list of proto files
    code_proto_list = []

    # Handle the DITA files
    for file in os.scandir(dita_location):
        if (file.path.endswith(".dita")) and not file.path.startswith(dita_location + "\enum_") and not file.path.startswith(dita_location + "\\rtc_") and file.is_file():
            print(file.path)
            dita_file_list.append(file.path)
            with open(file.path, encoding='utf8') as f:
                content = f.read()
                # Use substring methods to get the proto from DITA
                # Here, we assume that the DITA file contains a single codeblock for each programming language
                after_codeblock_start_tag = re.split('<codeblock props="windows" outputclass="language-cpp">',
                                                     content)
                try:
                    before_codeblock_end_tag = re.split('</codeblock>', after_codeblock_start_tag[1])
                    proto_text = before_codeblock_end_tag[0]
                except IndexError:
                    proto_text = "Error: No prototype"

                print(proto_text)
                dita_proto_list.append(proto_text)

    dictionary = dict(zip(dita_file_list, dita_proto_list))