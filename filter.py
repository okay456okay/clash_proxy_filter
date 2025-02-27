# coding=utf-8
import yaml
import requests
import sys

def process_yaml_from_url(url, output_file):
    try:
        # 从URL获取YAML内容
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败则抛出异常

        # 解析YAML内容
        data = yaml.safe_load(response.text)

        # 找出所有包含HongKong或HK的代理名称
        hk_proxies = []
        filtered_proxies = []

        for proxy in data.get('proxies', []):
            if isinstance(proxy, dict) and 'name' in proxy:
                name = proxy['name']
                if 'HongKong' in name or 'HK' in name:
                    hk_proxies.append(name)
                else:
                    filtered_proxies.append(proxy)

        # 更新代理列表
        data['proxies'] = filtered_proxies

        # 更新代理组列表，移除包含HongKong或HK的代理
        for group in data.get('proxy-groups', []):
            if isinstance(group, dict) and 'proxies' in group:
                group['proxies'] = [p for p in group['proxies'] if p not in hk_proxies]

        # 写入新的YAML文件
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"成功处理YAML文件并保存到 {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"获取URL内容失败: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"解析YAML失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python filter.py <yaml_url> <output_file>")
        sys.exit(1)

    yaml_url = sys.argv[1]
    output_file = sys.argv[2]

    process_yaml_from_url(yaml_url, output_file)