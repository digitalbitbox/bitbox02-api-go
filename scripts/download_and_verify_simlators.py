# Copyright 2024 Shift Crypto AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import requests
import gnupg

# Constants
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "BitBoxSwiss"
REPO_NAME = "bitbox02-firmware"
TAG_PREFIX = "firmware/"
DOWNLOAD_DIR = "downloads"

# security@shiftcrypto.ch pubkey
PUB_KEY = '''
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
jLZugv6bMuMLjA==
=0krM
-----END PGP PUBLIC KEY BLOCK-----
'''

# Initialize GPG
gpg = gnupg.GPG()

def import_public_key(pub_key):
    result = gpg.import_keys(pub_key)
    if result.count == 0:
        raise Exception("Failed to import public key")

def download_file(url, dest_path):
    if os.path.isfile(dest_path):
        print(f"File already exists, skipping. {dest_path}")
        return
    response = requests.get(url)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        f.write(response.content)

def verify_signature(sig_path, file_path):
    with open(sig_path, 'rb') as sig_file:
        verified = gpg.verify_file(sig_file, file_path)
        if not verified:
            raise Exception(f"Signature verification failed for {file_path}")

def download_and_verify_assets():
    # Get list of releases
    releases_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    response = requests.get(releases_url)
    response.raise_for_status()
    releases = response.json()

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    for release in releases:
        if release['tag_name'].startswith(TAG_PREFIX):
            sig_assets = [asset for asset in release['assets'] if asset['name'].endswith('.asc')]
            print(f"Found {len(sig_assets)} signatures in release {release['tag_name']}")
            for asset in sig_assets:
                asset_url = asset['browser_download_url']
                asset_name = asset['name']
                asset_path = os.path.join(DOWNLOAD_DIR, asset_name)

                print(f"Downloading {asset_name} from {asset_url}")
                download_file(asset_url, asset_path)

                binary_name = asset_name[:-4]
                binary_path = os.path.join(DOWNLOAD_DIR, binary_name)
                binary_url = asset_url[:-4]
                print(f"Downloading {binary_name} from {binary_url}")
                download_file(binary_url, binary_path)

                print(f"Verifying {asset_name}")
                verify_signature(asset_path, binary_path)

if __name__ == "__main__":
    import_public_key(PUB_KEY)
    download_and_verify_assets()
    print("Download and verification complete")
