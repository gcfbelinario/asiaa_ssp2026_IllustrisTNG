# import tools here
import requests
import os

# request specifications
API_KEY = "2b53ab2137136266330440cdef40b53a"
HEADERS = {"api-key": API_KEY}


# target data
SIMULATION = "TNG100-1"
SNAPSHOT = 50


# make directory for data storage
OUTPUT_DIR = f"/theory/lts/gbelinar/IllustrisTNG/{SIMULATION}_groupcat_{SNAPSHOT}"
os.makedirs(OUTPUT_DIR, exist_ok=True)


snapshot_url = f"https://www.tng-project.org/api/{SIMULATION}/snapshots/{SNAPSHOT}/"
response = requests.get(snapshot_url, headers=HEADERS)
response.raise_for_status()
metadata = response.json()                                                                  # extract metadata of the chosen snapshot

print("Redshift:", metadata["redshift"])                                                    # verify redshift of the snapshot


# isolate Group Catalog
groupcat_url = metadata["files"]["groupcat"]
print("Group Catalog URL:", groupcat_url)


# inspect list of group catalog files
response = requests.get(groupcat_url, headers=HEADERS)
response.raise_for_status()
groupcat_info = response.json()

# list of URL to Group Catalog files 
files = groupcat_info["files"]

print(f"Number of Group Catalog files: {len(files)}")

# BEGIN FILE DOWNLOADS

for url in files:

    # Extract filename from URL
    filename = url.split("/")[-1]

    filepath = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        print(f"The file {filename} already exists. Proceeding to next file ...")
        continue

    print(f"Downloading {filename} ...")

    r = requests.get(url, headers=HEADERS, stream=True)
    r.raise_for_status()

    with open(filepath, "wb") as f:

        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
            
    print(f"Downloading {filename} complete.")

print(f"Downloading {SIMULATION}_groupcat_{SNAPSHOT} complete.")

