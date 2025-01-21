import re

def replace_punctuation_in_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换中文逗号和句号
    new_content = re.sub(r'，', ', ', content)  # 中文逗号替换为英文逗号加空格
    new_content = re.sub(r'。', '. ', new_content)  # 中文句号替换为英文句号加空格
    new_content = re.sub(r'：', ': ', new_content)  # 中文句号替换为英文句号加空格
    new_content = re.sub(r'（', ' (', new_content)  # 中文句号替换为英文句号加空格）
    new_content = re.sub(r'）', ') ', new_content)  # 中文句号替换为英文句号加空格
    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"文件 {file_path} 已修改完成！")

# 替换的文件路径
file_path1 = "./bt_hci_cmd_create.txt"  # 将 'your_file.txt' 替换为你的文件路径
file_path2 = "./nrf_note.txt"  # 将 'your_file.txt' 替换为你的文件路径
# 调用函数修改文件
replace_punctuation_in_file(file_path1)
replace_punctuation_in_file(file_path2)