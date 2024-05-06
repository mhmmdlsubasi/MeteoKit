from datetime import datetime
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


from mgm_request import *
radar = Radar()

def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
        file_hash = hashlib.md5(file_content).hexdigest()
    return file_hash

def process_file(filename, path, hash_new):
    file_path = os.path.join(path, filename)
    file_hash = calculate_hash(file_path)
    if file_hash == hash_new:
        return True
    return False

def save(province,image_type,path,response):
    now = datetime.now()
    filename = f"{province}_{image_type}_{now:%Y%m%d%H%M}.jpg"
    directory = os.path.join(path,filename)
    with open(directory, 'wb') as f:
        f.write(response.content)
    print("Saved ", filename)

def run(province,image_type,path):
    response = radar.get_image(province=province, image_type=image_type)
    hash_new = hashlib.md5(response.content).hexdigest()

    path += f"/{province}/{image_type}/"
    if not os.path.exists(path): os.makedirs(path)
    
    results = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(path):
            if filename.endswith(".jpg"):
                future = executor.submit(process_file, filename, path, hash_new)
                futures.append(future)
        for future in futures:
            result = future.result()  # İşlemin tamamlanmasını bekler ve sonucu alır
            results.append(result)
    # for filename in os.listdir(path):
    #     if filename.endswith(".jpg"):
    #         result = process_file(filename, path, hash_new)
    #         results.append(result)
            
    if not any(results):
        save(province, image_type, path, response)

def main():
    radar_codes = radar.radar_codes
    image_types = radar.image_types
    while 1:
        run("Ankara","ppi","./output")
        # with ProcessPoolExecutor() as executor:
        #     executor.submit(run, "Ankara", "ppi", "./output")

        # with ProcessPoolExecutor() as executor:
        #     for province in radar_codes.values():
        #         if province == "Birleştirilmiş Görüntü":
        #             executor.submit(run, province, "ppi", "./output/radar")
        #             continue
        #         for image_type in image_types:
        #             executor.submit(run, province, image_type, "./output/radar")
                    
                    
        # for province in radar_codes.values():
        #     if not province == "Birleştirilmiş Görüntü":
        #         for image_type in image_types:
        #             run(province,image_type,"./output")

if __name__ == '__main__':
    main()