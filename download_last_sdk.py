# This master run test file do following tasks :
# 	- clone test from git and replace code at local
# 	- download portable build from jenkin to local (run test with this build)
# 	- run test in server with batch mode and generate HTML report
# 	- deploy the test result to predefine place and use HTML Publisher from Jenkin to show up on Jenkin

# Requirement for this controler
# 	- Support for multiple application : ControlPanel, Pure.EGG, Composer, Emokey
# 	- Support running for multiple platform : Window, Mac, Unix
#	- Support for input agruments so this script could be use from Jenkin for multiple job


import requests
import zipfile
import os
import time
import subprocess as sub
import base64
import shutil
import glob
import sys, getopt

# from slacker import Slacker
from bs4 import BeautifulSoup
from bs4 import NavigableString


username = 'tanpham'
password = '12345678'


# This function download and extract lastest build from jenkin to local machine
def download_and_extract_last_success_buld_from_jenkin(job_name, platform):

	url = 'http://builds.emotiv.com:8090/job/{0}/lastSuccessfulBuild/artifact/'.format(job_name)

	r = requests.get(url, auth=(username,password))

	soup = BeautifulSoup(r.text, 'lxml')

	# print soup.prettify()

	title = soup.find('title')

	build_num = title.text.split("build")[1].split("_")[0]

	# download url 
	dll_url = 'http://builds.emotiv.com:8090/job/{0}/lastSuccessfulBuild/artifact/build-jenkins-'.format(job_name) + build_num + '/Libs/Release/edk.dll'
	lib_url = 'http://builds.emotiv.com:8090/job/{0}/lastSuccessfulBuild/artifact/build-jenkins-'.format(job_name) + build_num + '/Libs/Release/edk.lib'
	
	
	# try with local
	# org_dll = 'C:\\Jenkins\\edk.dll'
	# org_lib = 'C:\\Jenkins\\edk.lib'
	

	dll_local_path = "C:\\Jenkins\\workspace\\EDK_Auto_Test\\SdkAutoTest\\bin\\x86\\edk.dll"
	# dll_local_path = "C:\\Jenkins\\workspace\\EDK_Auto_Test\\SdkAutoTest\\bin\\x86\\edk.dll"
	lib_local_path = "C:\\Jenkins\workspace\\EDK_Auto_Test\\lib\\win32\\edk.lib"


	# download_sdk_and_save_to_build_local(dll_url, dll_local_path)
	# download_sdk_and_save_to_build_local(lib_url, lib_local_path)


# 	copy_dll_lib_local(org_dll, dll_local_path)
# 	copy_dll_lib_local(org_lib, lib_local_path)


# def copy_dll_lib_local(org_path, local_path):




def download_sdk_and_save_to_build_local(url_path, local_path):
	
	print url_path
	print local_path
	
	# remove file
	try:
		os.remove(local_path)
	except OSError:
		pass

	# request file from url
	r = requests.get(url_path, auth=(username,password), stream=True)
	dump = r.raw

	# save file to local
	with open(local_path, 'wb') as local_path :
		shutil.copyfileobj(dump, local_path)
	del dump
	

def main():

	opts, args = getopt.getopt(sys.argv[1:],"j:p:")

	jenkin_job = ''
	platform = ''

	# print opts

	for o,a in opts:
		if o == '-j':
			jenkin_job = a
		if o == '-p':
			platform = a


	print jenkin_job
	print platform


	download_and_extract_last_success_buld_from_jenkin(jenkin_job, platform)

	
main()

# job_name = 'EDK_v3.4_Windows_32bit'
# platform = 'win'
# download_and_extract_last_success_buld_from_jenkin(job_name, platform)
