#!/usr/bin/python
# coding: utf-8
import subprocess

def remove_null_byte():
	subprocess.call(["sh", "remove_null_byte.sh"])
