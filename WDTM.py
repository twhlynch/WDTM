import argparse, UnityPy, json, subprocess, shutil

def decompile(apk_path):
    print(f"Decompiling {apk_path} into {apk_path[:-4]}")
    sp = subprocess.Popen(["apktool", "d", "-f", apk_path], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

def main(original_apk, modified_apk):
    print(f"Original APK: {original_apk}")
    print(f"Modified APK: {modified_apk}")
    
    decompile(original_apk)
    decompile(modified_apk)

    original_env = UnityPy.load(f"{original_apk[:-4]}/assets/bin/Data/data.unity3d")
    modified_env = UnityPy.load(f"{modified_apk[:-4]}/assets/bin/Data/data.unity3d")

    with open("changes.log", 'w') as output_file:
        diffs = ""
        for obj_index in range(len(original_env.objects)):
            original_obj = original_env.objects[obj_index]
            if original_obj.type.name == "GameObject":
                original_data = original_obj.read()
                modified_obj = modified_env.objects[obj_index]
                modified_data = modified_obj.read()
                if hasattr(original_data, 'm_IsActive') and hasattr(modified_data, 'm_IsActive'):
                    if original_data.m_IsActive != modified_data.m_IsActive:
                        diffs += f"{original_data.name.ljust(50)} > {modified_data.m_IsActive}\n"

        if diffs != "":
            output_file.write(diffs)
    
    shutil.rmtree(f"{original_apk[:-4]}")
    shutil.rmtree(f"{modified_apk[:-4]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="What Did They Modify?")
    parser.add_argument("original_apk", help="Path to the original APK file")
    parser.add_argument("modified_apk", help="Path to the modified APK file")

    args = parser.parse_args()

    main(args.original_apk, args.modified_apk)
