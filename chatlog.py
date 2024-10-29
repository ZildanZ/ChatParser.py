import re

def extract_chat(file_path):
    encodings = ['utf-8', 'latin-1', 'windows-1252']  # Daftar encoding yang akan dicoba
    lines = None
    
    # Coba membaca file dengan beberapa encoding
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
            break  # Jika berhasil membaca, keluar dari loop
        except UnicodeDecodeError:
            continue  # Jika gagal, coba encoding berikutnya

    if lines is None:
        raise Exception("Tidak dapat membaca file dengan encoding yang diberikan.")

    chat_dialogs = []
    me_pattern = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] ([^ ]+_[^ ]+) (.+)$')
    says_pattern = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] ([^ ]+_[^ ]+)\(\d+\) says : (.+)$')
    do_pattern = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] (.+) \(([^ ]+_[^ ]+)\)$')
    iklan_pattern = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] \{7fff00\}\[ IKLAN \].+')
    pm_pattern = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] \(\(PM From .+\)\)$')

    for line in lines:
        if iklan_pattern.match(line) or pm_pattern.match(line):
            continue

        if says_pattern.match(line):
            cleaned_line = says_pattern.sub(r'\1 says : \2', line).strip()
            chat_dialogs.append(cleaned_line)

        elif me_pattern.match(line):
            cleaned_line = me_pattern.sub(r'*\1 \2', line).strip()
            chat_dialogs.append(cleaned_line)

        elif do_pattern.match(line):
            cleaned_line = do_pattern.sub(r'*\1 (\2)', line).strip()
            chat_dialogs.append(cleaned_line)

    return chat_dialogs

def main():
    print("  ____ _           _   _     ___   ____   ____                           ")
    print(" / ___| |__   __ _| |_| |   / _ \\ / ___| |  _ \\ __ _ _ __ ___  ___ _ __ ")
    print("| |   | '_ \\ / _` | __| |  | | | | |  _  | |_) / _` | '__/ __|/ _ \\ '__|")
    print("| |___| | | | (_| | |_| |__| |_| | |_| | |  __/ (_| | |  \\__ \\  __/ |   ")
    print(" \\____|_| |_|\\__,_|\\__|_____\\___/ \\____| |_|   \\__,_|_|  |___/\\___|_|   ")
    print("author by Zildan Security\n")
    
    file_path = input("Masukkan path file chatlog yang ingin dirapikan: ")

    try:
        filtered_chat = extract_chat(file_path)
        output_file = "cleaned_chatlog.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for chat in filtered_chat:
                f.write(chat + '\n')

        print(f"\nChatlog berhasil dirapikan dan disimpan ke '{output_file}'")
    except FileNotFoundError:
        print("Error: File tidak ditemukan. Pastikan path file yang dimasukkan benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
