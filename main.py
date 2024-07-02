import requests
import json
import os


def read_package_index_url(file_path):
    """
    读取包含URL的JSON文件并解析为字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            package_index_url = json.load(file)
        return package_index_url
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")


def select_url(package_index_url):
    """
    让用户选择预定义的URL或输入自定义URL
    """
    print("\n可用的URL列表:")
    keys = list(package_index_url.keys())
    for i, key in enumerate(keys, 1):
        print(f"\t{i}. {key}: {package_index_url[key]}")

    print(f"\t{len(keys) + 1}. 输入自定义URL")

    while True:
        try:
            selected_index = int(input(f"请选择URL: "))
            if 1 <= selected_index <= len(keys):
                return package_index_url[keys[selected_index - 1]]
            elif selected_index == len(keys) + 1:
                custom_url = input("请输入自定义URL: ")
                return custom_url
            else:
                print("选择无效，请输入有效的数字。")
        except ValueError:
            print("无效输入，请输入数字。")


def download_and_parse_json(url):
    """
    发送 HTTP GET 请求并解析 JSON 数据
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")


def print_package_info(package):
    """
    打印包的信息
    """
    package_name = package['name']
    print('=' * 60)
    print(package_name.center(60))
    print('=' * 60)
    print(f"维护: {package['maintainer']}")
    print(f"WEB: {package['websiteURL']}")


def print_available_versions(platforms):
    """
    打印可用版本信息，从高到低排序，并分为三列显示
    """
    sorted_platforms = sorted(platforms, key=lambda x: x['version'], reverse=True)
    print("\n可用版本:")

    num_versions = len(sorted_platforms)
    num_columns = 3
    num_rows = (num_versions + num_columns - 1) // num_columns  # 计算行数

    for row in range(num_rows):
        for col in range(num_columns):
            index = row + col * num_rows
            if index < num_versions:
                print(f"\t{index + 1}. {sorted_platforms[index]['version']:<15}", end='')
        print()

    return sorted_platforms


def get_selected_version(sorted_platforms):
    """
    获取用户选择的版本
    """
    latest_version = sorted_platforms[0]['version']
    while True:
        try:
            selected_index = input(f"请选择版本 (默认: {latest_version}): ")
            if not selected_index:
                return latest_version
            selected_index = int(selected_index)
            if 1 <= selected_index <= len(sorted_platforms):
                return sorted_platforms[selected_index - 1]['version']
            else:
                print("选择无效，请输入有效的数字。")
        except ValueError:
            print("无效输入，请输入数字。")


def get_download_list(platforms, tools, host, select_version):
    """
    获取下载列表
    """
    download_list = {}
    tools_dependencies = []

    for item in platforms:
        if item['version'] == select_version:
            download_list[item['name']] = item['url']
            tools_dependencies = item['toolsDependencies']
            break

    for item in tools_dependencies:
        for tool in tools:
            if item['name'] == tool['name'] and item['version'] == tool['version']:
                for sys in tool['systems']:
                    if sys['host'] == host:
                        download_list[item['name']] = sys['url']
    return download_list


def print_available_hosts(tools):
    """
    打印可用的 host 类型，并返回排序后的列表
    """
    hosts = set()
    for tool in tools:
        for sys in tool['systems']:
            hosts.add(sys['host'])

    sorted_hosts = sorted(hosts)

    return sorted_hosts


def get_selected_host(available_hosts):
    """
    获取用户选择的 host 类型
    """
    print("\n可选主机架构:")
    for i, host in enumerate(available_hosts, 1):
        print(f"\t{i}. {host}")

    while True:
        try:
            selected_host_index = int(input(f"请选择主机架构(1-{len(available_hosts)}): "))
            if 1 <= selected_host_index <= len(available_hosts):
                return available_hosts[selected_host_index - 1]
            else:
                print("选择无效，请输入有效的数字。")
        except ValueError:
            print("无效输入，请输入数字。")


def print_download_links(download_list):
    """
    按指定格式打印下载链接
    """
    print("\n" + "=" * 60)
    for name, url in download_list.items():
        print(f"{name}")
    print("=" * 60)
    for url in download_list.values():
        print(url)
    print("=" * 60)


def print_tips():
    """
    打印Arduino默认存放路径提示信息
    """
    local_app_data = os.getenv('LOCALAPPDATA')
    arduino_dir = os.path.join(local_app_data, 'Arduino15')
    staging_packages_dir = os.path.join(arduino_dir, 'staging', 'packages')

    print("\n" + "=" * 60)
    print("Tips: 下面是Arduino默认的存放路径")
    print(arduino_dir)
    print(staging_packages_dir)
    print("=" * 60 + "\n")


def main():
    # 读取packageIndexUrl.json文件
    file_path = 'packageIndexUrl.json'
    package_index_url = read_package_index_url(file_path)

    if not package_index_url:
        return

    # 选择URL
    url = select_url(package_index_url)

    json_data = download_and_parse_json(url)

    if not json_data:
        return

    json_data = json_data["packages"][0]
    platforms = json_data['platforms']
    tools = json_data['tools']

    print_package_info(json_data)

    sorted_platforms = print_available_versions(platforms)
    select_version = get_selected_version(sorted_platforms)

    available_hosts = print_available_hosts(tools)
    selected_host = get_selected_host(available_hosts)

    download_list = get_download_list(platforms, tools, selected_host, select_version)

    print(f"\n版本 {select_version} 和 host {selected_host} 依赖如下:")
    print_download_links(download_list)

    print_tips()


if __name__ == "__main__":
    main()
