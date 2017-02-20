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
def download_and_extract_last_success_buld_from_jenkin(job_test, job_name, platform):

	url = 'http://builds.emotiv.com:8090/job/{0}/lastSuccessfulBuild/artifact/'.format(job_name)
	
	r = requests.get(url, auth=(username,password))
	
	soup = BeautifulSoup(r.text, 'lxml')
	
	title = soup.find('title')

	# print title.text
	
	global build_number
	
	build_number = title.text.split("build")[1].split("_")[0]

	print build_number

	url_path = 'http://builds.emotiv.com:8090/job/{0}/lastSuccessfulBuild/artifact/*zip*/archive.zip'.format(job_name)
	
	local_path = "C:\\Jenkins\\workspace\\{0}\\archive.zip".format(job_test)

	extract_dir = "C:\\Jenkins\\workspace\\{0}".format(job_test)

	download_save_and_extract_to_local(url_path, local_path, extract_dir)

	if job_test == 'PureEEG_Auto_Test':
		return "C:\\Jenkins\\workspace\\{0}\\archive\\build-jenkins-{1}\\Programs\\Release\\Applications".format(job_test, build_number)
	
	if job_test == 'ControlPanel_Auto_Test':
		return 	"C:\\Jenkins\\workspace\\ControlPanel_Auto_Test\\archive\\build-jenkins-{0}\\Programs\\Release".format(build_number)



def download_save_and_extract_to_local(url_path, local_path, extract_dir):
	
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
	with open(local_path, 'wb') as zf :
		shutil.copyfileobj(dump, zf)
	del dump

	zip_ref = zipfile.ZipFile(local_path, 'r')
	zip_ref.extractall(extract_dir)
	zip_ref.close()


# This function do run test in batch mode with lastest app downloaded from jenkin
# The test result will be in the same folder with software
def run_test_in_batch_mode(app_path, app_name, jenkin_job, platform,job_test):

	if platform == 'win':
		# add UAT and Path to squish
		os.system('C:\\Qt6102\\bin\\squishserver --config addAUT "{0}" "{1}"'.format(app_name, app_path))
		os.system('C:\\Qt6102\\bin\\squishserver --config addAppPath "{0}"'.format(app_path))
		
		# start squish server
		os.system('start C:\\Qt6102\\bin\\squishserver')
		
		# delete all to ensure nothing inside test result folder
		folder = 'C:\\Jenkins\\workspace\\{0}\\test_result'.format(job_test)

	
	# clearn up test result folder
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)


	if platform == 'win':

		test_result = 'C:\\Jenkins\\workspace\\{0}\\test_result'.format(job_test)

		# run test
		os.system('C:\\Qt6102\\bin\\squishrunner --testsuite C:\\Jenkins\\workspace\\{2}\\suite_{1} --reportgen "html,{0}"'.format(test_result, app_name, job_test))

		# convert test result to HTML
		os.system('C:\\Qt6102\\bin\\squishserver --stop')

		# modify test result with build number and appname so test result will be more clear
		index_file = test_result + '\\index.html'

	add_build_number_and_product_name(index_file, jenkin_job, build_number)



def get_last_test_script(platform):

	if platform == 'win':

		# fetch from origin to local
		os.system('cd C:\\emotive-automation-test-script && git fetch origin')

		# reset local
		os.system('cd C:\\emotive-automation-test-script && git reset --hard origin/master')



# Notify to slack about automation test already finish
def notify_to_slack(message):
	
	# Create slacker	
	slack = Slacker('xoxp-2310266911-79868263043-83121325842-6b03a445372cb4c7d6d5cfc9ff2d67f6')

	# Send a message to #general channel
	slack.chat.post_message('#bobthebuilder-is-back', message)


def add_build_number_and_product_name(index_file, jenkin_job, build_number):

	soup = BeautifulSoup(open(index_file),'lxml')
	result = soup.find('h3')
	result.extract()
	new_h3 = soup.new_tag('h3', class_ = 'ui top attached header')
	soup.body.div.insert(0, new_h3)

	soup.body.div.h3.insert(0, NavigableString('Test result {0} build {1}'.format(jenkin_job, build_number)))

	# save the file again
	with open(index_file, "w") as outf:
		outf.write(str(soup))


def main():

	opts, args = getopt.getopt(sys.argv[1:],"t:b:a:p:")

	job_test = ''
	job_build = ''
	app_name = ''
	platform = ''

	# print opts

	for o,a in opts:
		if o == '-t':
			job_test = a
		if o == '-b':
			job_build = a
		if o == '-a':
			app_name = a
		if o == '-p':
			platform = a

	print job_test
	print job_build
	print app_name
	print platform

	app_path = download_and_extract_last_success_buld_from_jenkin(job_test, job_build, platform)

	print app_path

	# run test
	run_test_in_batch_mode(app_path, app_name, job_build, platform,job_test)

	# message = url to test result
	# only put result to slack when all thing come to stable
	# notify_to_slack()

	
main()
