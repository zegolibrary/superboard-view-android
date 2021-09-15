import os
import json
import sys
import shutil
import urllib2
import zipfile
import tarfile
import subprocess
import ssl
import argparse

PROJECT_NEW_URL = 'https://artifact-master.zego.cloud/generic/superboard/public/android/feature/{}/zegosuperboard.aar?version={}'
SUB_DIR_NAMES = ['online', 'test']

THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def __parse_args(args):
    args = args[1:]
    parser = argparse.ArgumentParser(description='The root build script.')

    parser.add_argument('--sdk_version', type=str, default='')

    return parser.parse_args(args)


def main(argv):
    args = __parse_args(argv)
    print("arguments: {}".format(args))
    print(sys.version)

    if len(args.sdk_version) == 0:
        raise Exception("SDK URL must not be EMPTY!")

    dst_libs_path = os.path.join(THIS_SCRIPT_PATH, '..', 'superboardsdk')

    for sub_dir in SUB_DIR_NAMES:
        oss_url = PROJECT_NEW_URL.format(sub_dir, args.sdk_version)
        artifact_name = oss_url.split('/')[-1]
        artifact_name = artifact_name.split('?')[0] # remove url version
        u = None
        try:
            request = urllib2.Request(oss_url)
            print('\n --> Request: "{}"'.format(oss_url))
            context = ssl._create_unverified_context()
            u = urllib2.urlopen(request, context=context)
            print(' <-- Response: "{}"'.format(u.code))
        except :
            pass
        if u is not None and u.code == 200:
            break

    artifact_path = os.path.join(THIS_SCRIPT_PATH, artifact_name)
    with open(artifact_path, 'wb') as fw:
        fw.write(u.read())

    print("Download SDK success")

    shutil.copy(os.path.join(artifact_path), os.path.join(dst_libs_path))
    os.remove(artifact_path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
