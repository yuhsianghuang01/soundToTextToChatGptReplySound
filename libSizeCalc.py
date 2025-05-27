import requests
import json

def get_package_info(package_name):
    """從 PyPI 獲取指定庫的資訊"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"無法找到庫 {package_name} 的資訊，請檢查名稱是否正確。")
        return None

def calculate_total_size(package_name, visited=None):
    """計算指定庫及其相依庫的總大小"""
    if visited is None:
        visited = set()

    if package_name in visited:
        return 0  # 避免重複計算

    visited.add(package_name)
    package_info = get_package_info(package_name)
    if not package_info:
        return 0

    # 計算當前庫的大小
    total_size = 0
    releases = package_info.get("releases", {})
    for version, files in releases.items():
        for file in files:
            size = file.get("size", 0)
            total_size += size

    # 遞迴計算相依庫的大小
    requires_dist = package_info["info"].get("requires_dist", [])
    if requires_dist:
        for dependency in requires_dist:
            dep_name = dependency.split()[0]  # 提取相依庫名稱
            total_size += calculate_total_size(dep_name, visited)

    return total_size

def main():
    package_name = input("請輸入要查詢的庫名稱：")
    print("正在計算大小，請稍候...")
    total_size = calculate_total_size(package_name)
    if total_size > 0:
        print(f"庫 {package_name} 及其相依庫的總大小約為 {total_size / (1024 * 1024):.2f} MB")
    else:
        print("無法計算大小，請檢查庫名稱是否正確。")

if __name__ == "__main__":
    main()
