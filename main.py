# This is a sample Python script.
import hashlib
import os, pathlib
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_file_hash(filepath):
    # to get file hash of filepath
    filehash = hashlib.sha256(filepath.encode('utf-8')).hexdigest()
    return filehash

def absolute_file_path():

    return pathlib.Path(__file__).parent.absolute()


def delete_if_baseline_already_exist():
    if os.path.exists("baseline.txt"):
        os.remove("baseline.txt")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_hash_dict = {}
    file_hash_list = []
    baseline_dict = {}

    print("")
    print("What do you want to do?")
    print("A) Collect new Baseline")
    print("B) Begin monitoring files with current Baseline\n")
    response = input("What is your option? (A/B): ")

    if response.upper() == 'A':
        delete_if_baseline_already_exist()

        for file in os.listdir(absolute_file_path()):
            #for files in current directory of FileIntegrityMonitor.py
            if file.endswith(".txt") and file != 'baseline.txt':
                contents = open(file, 'r')
                M = contents.readline()
                contents.close()
                #file_hash_list.append(f'{file} | {get_file_hash(M)}\n')

                #print(f'{file} | {get_file_hash(M)}')
                out = open("baseline.txt", 'a')
                out.write(f'{file} | {get_file_hash(M)}\n')
                out.close()


    elif response.upper() == 'B':
        while True:
            import time
            baseline = open("baseline.txt", 'r')
            for line in baseline:
                k, v = line.strip().split("|")
                baseline_dict[k.strip()] = v.strip()
            baseline.close()

            # notify if file has been changed or added
            for file in os.listdir(absolute_file_path()):
                if file.endswith(".txt") and file != 'baseline.txt':
                    content = open(file, 'r')
                    M = content.readline()
                    file_hash_dict[file] = get_file_hash(M)
                    try:
                            if file_hash_dict[file] != baseline_dict[file]:
                                print(f"{file} has been compromised!\n")
                                time.sleep(2)
                    except(KeyError) as e:
                            # new file has been added into this folder, Inform user!!!
                            print(f'New file {e} has been added into this folder!\n')
                            time.sleep(2)

            # notify if new file has been removed
            for key in baseline_dict:
                import time
                try:
                    file_hash_dict[key]
                except KeyError as e:
                    # new file has been removed from this folder, Inform user!!!
                    print(f'{e} has been deleted from this folder!\n')
                    time.sleep(2)















