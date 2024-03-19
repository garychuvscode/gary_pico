# 定義一個字典，用於儲存一些虛構的人物及其相關的職業
people_jobs = {
    "Alice": "Engineer",
    "Bob": "Doctor",
    "Charlie": "Artist",
    "Diana": "Scientist"
}

# 使用 .keys() 方法獲取所有人名（字典的鍵）
print("所有人名（字典的鍵）:")
for name in people_jobs.keys():
    print(name)

# 使用 .values() 方法獲取所有職業（字典的值）
print("\n所有職業（字典的值）:")
for job in people_jobs.values():
    print(job)

# 使用 .items() 方法同時獲取人名和職業（字典的鍵值對）
print("\n人名和對應的職業（字典的鍵值對）:")
for name, job in people_jobs.items():
    print(f"{name} 是一位 {job}")

# 搜尋示例：檢查某個人名是否在字典的鍵中
search_name = "Alice"
if search_name in people_jobs.keys():
    print(f"\n找到了 {search_name}，他/她是一位 {people_jobs[search_name]}")
else:
    print(f"\n沒有找到 {search_name}")

# 這些基本的字典操作在許多場景中都非常有用，比如數據處理、設置配置選項、快速查找/搜尋、數據整合等。

# ===============

# 要搜尋的名字和職業
search_name = "Alice"
search_job = "Engineer"

# 使用 .items() 方法同時獲取人名和職業，並檢查是否符合搜尋條件
found = False  # 用於標記是否找到匹配項
for name, job in people_jobs.items():
    if name == search_name and job == search_job:
        found = True  # 找到匹配項，更新標記
        break  # 跳出循環

# 根據搜尋結果輸出信息
if found:
    print(f"找到了名字為 {search_name} 且職業為 {search_job} 的人")
else:
    print(f"沒有找到名字為 {search_name} 且職業為 {search_job} 的人")

# 這種搜尋方法允許我們在字典中根據多個條件進行過濾和搜尋，適用於需要對數據進行精細化管理和查詢的場景。