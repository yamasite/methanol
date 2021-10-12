#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# Developed by Lutkin Wang
#
# Story: Replace the prototype section so that manual copy & paste is no longer needed
#
# <section id="prototype">
#         <p props="rtc-ng" outputclass="codeblock">
#                 <codeblock props="android" outputclass="language-java">public abstract void onMetadataReceived(byte[] buffer, int uid, long timeStampMs);</codeblock>
#                 <codeblock props="ios mac" outputclass="language-objectivec">- (void)receiveMetadata:(NSData * _Nonnull)data
#     fromUser:(NSInteger)uid atTimestamp:(NSTimeInterval)timestamp;</codeblock>
#             </p>
#         <p props="rtc" outputclass="codeblock">
#                 <codeblock props="android" outputclass="language-java"/>
#                 <codeblock props="ios mac" outputclass="language-objectivec"/>
#                 <codeblock props="windows unity" outputclass="language-cpp">virtual void onMetadataReceived(const Metadata &amp;metadata) = 0;
#     };</codeblock>
#                 <codeblock props="electron" outputclass="language-typescript">on(evt: EngineEvents.RECEIVE_METADATA, cb: (
#     metadata: Metadata
#     ) => void): this;</codeblock>
#                 <codeblock props="rn" outputclass="language-typescript"/>
#                 <codeblock props="flutter" outputclass="language-dart"/>
#         </p>
#         </section>
#
# from: C:\Users\WL\Documents\GitHub\doc_source\dita\RTC\API\xxx.dita
#
# with: C:\Users\WL\Documents\GitHub\doc_source\en-US\dita\RTC\API\xxx.dita
#

import xml.etree.ElementTree as ET
import os
from os import path

# cn_dir = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\API"
cn_dir = "D:\\github_lucas\\doc_source\\dita\\RTC\\API"

# en_dir = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"
en_dir = "D:\\github_lucas\\doc_source\\en-US\\dita\\RTC\\API"

cn_proto_section_obj = None
en_proto_section_obj = None
en_dita_file_tree = None

# Copy cn protos to en
for file_name in os.listdir(cn_dir):
    if file_name.startswith("api_")  or file_name.startswith("class_"):

        try:
            cn_path = path.join(cn_dir, file_name)
            cn_dita_file_tree = ET.parse(cn_path)
            cn_dita_file_root = cn_dita_file_tree.getroot()
        except ET.ParseError as e:
            print("Parse error for: " + file_name + " Code: " + str(e.code) + " Position: " + str(e.position))

        en_path = path.join(en_dir, file_name)

        try:
            en_dita_file_tree = ET.parse(en_path)
            en_dita_file_root = en_dita_file_tree.getroot()
        except FileNotFoundError as e:
            print("File not found in en: " + file_name)

        except ET.ParseError as e:
            print("Parse error for: " + file_name + " Code: " + str(e.code) + " Position: " + str(e.position))


        for section in cn_dita_file_root.iter("section"):
            if section.get("id") == "prototype":
                cn_proto_section_obj = section

        refbody = en_dita_file_root.find("./refbody")

        for section in en_dita_file_root.iter("section"):
            if section.get("id") == "prototype":
                refbody.remove(section)
                refbody.insert(0, cn_proto_section_obj)

        en_dita_file_tree.write(en_dir + "//" + file_name)

        header = """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">\n"""

        with open(en_dir + "//" + file_name, "r") as f:
            text = header + f.read()

        with open(en_dir + "//" + file_name, "w") as f:
            f.write(text)









