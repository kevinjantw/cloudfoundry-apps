# -*- coding: utf8 -*-
import sys, os

if len(sys.argv) <= 2:
    print "\n"
    print "[deployInfo] Invalid command line arguments: need space and version number" + "\n"
    print "[deployInfo] example: python deploy.py production 1.0.0" + "\n"
    exit(0)
elif not sys.argv[1] in ["production", "stage", "develop"]:
    print "\n"
    print "[deployInfo] Invalid project space" + "\n"
    print "[deployInfo] example: production, stage, develop" + "\n"
    exit(0)
elif len(sys.argv[2]) != 5 or not str(sys.argv[2][0]).isdigit() or sys.argv[2][1] != '.' \
        or not str(sys.argv[2][2]).isdigit() or sys.argv[2][3] != '.' \
        or not str(sys.argv[2][4]).isdigit():
    print "\n"    	
    print "[deployInfo] Invalid version number format" + "\n"
    print "[deployInfo] example: 1.0.0" + "\n"
    exit(0)
space = sys.argv[1]
version = sys.argv[2]

deploy_dir = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
genManifestPath = deploy_dir + 'genManifest.sh'
os.chdir(deploy_dir)
gen_manifest_file = deploy_dir + 'manifest-' + space + '.yml'

f = open(gen_manifest_file, 'w')
f.write('applications:' + '\n')
f.write('- name: cf-service-postgresql-metering-' + version + '\n')
f.write('  version: ' + version + '\n')
f.write('  buildpack: ' + 'python_buildpack' + '\n')
f.write('  health-check-type: ' + 'process' + '\n')
f.write('  no-route: ' + 'true' + '\n')
f.write('  memory: ' + '1G' + '\n')
f.write('  disk_quota: ' + '2G' + '\n')
f.close()

while True:
    if os.path.exists(gen_manifest_file):
        if os.stat(gen_manifest_file).st_size != 0:
            break

app_name_list = [line.strip() for line in open(gen_manifest_file) if 'name' in line]
app_name = app_name_list[0].replace('-','',1).replace('name','').replace(':','').strip()
if not app_name:
    print "[deployInfo] No app name" + "\n"
    exit(0)

os.system('cf delete ' + app_name + ' -f')
os.system('cf push -f ' + gen_manifest_file)