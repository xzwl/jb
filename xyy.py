"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
小阅阅_V1.4
入口：https://wi53263.nnju.top:10258/yunonline/v1/auth/a736aa79132badffc48e4b380f21c7ac?codeurl=wi53263.nnju.top:10258&codeuserid=2&time=1693450574
抓包搜索关键词ysm_uid 取出ysm_uid的值即可

export ysm_uid=xxxxxxx
多账号用'===='隔开 例 账号1====账号2
"""
money_Withdrawal = 0  # 提现开关 1开启 0关闭
max_concurrency = 3  # 设置要运行的线程数(建议3线程)
key = ""  # 内置key 必填！！！ key为企业微信webhook机器人后面的 key

import json
import os
import random
import re
import threading
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse, parse_qs
from requests.exceptions import ConnectionError, Timeout
import requests

lock = threading.Lock()
max_retries = 3

def process_account(account, i):
    values = account.split('@')
    xyy_uid = values[0]
    print(f"\n=======开始执行账号{i}=======")
    print(f"unionid:{xyy_uid}")
    current_timestamp = int(time.time() * 1000)

    url = 'http://1693441346.pgvv.top/yunonline/v1/gold'

    headers = {
        'Cookie': f'ejectCode=1; ysm_uid={xyy_uid}',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
    }

    params = {
        'unionid': f'{xyy_uid}',
        'time': current_timestamp
    }

    response = requests.get(url, headers=headers, params=params).json()
    if response['errcode'] == 0:
        day_gold = response['data']['day_gold']
        day_read = response['data']['day_read']
        last_gold = response['data']['last_gold']
        remain_read = response['data']['remain_read']
        print(f'当前金币:{last_gold}\n今日阅读文章:{day_read} 剩余:{remain_read}')
        print(f"{'=' * 18}开始阅读文章{'=' * 18}")
        for i in range(33):
            checkDict = [
                'MzkxNTE3MzQ4MQ==',
                'Mzg5MjM0MDEwNw==',
                'MzUzODY4NzE2OQ==',
                'MzkyMjE3MzYxMg==',
                'MzkxNjMwNDIzOA==',
                'Mzg3NzUxMjc5Mg==',
                'Mzg4NTcwODE1NA==',
                'Mzk0ODIxODE4OQ==',
                'Mzg2NjUyMjI1NA==',
                'MzIzMDczODg4Mw==',
                'Mzg5ODUyMzYzMQ==',
                'MzU0NzI5Mjc4OQ==',
                'Mzg5MDgxODAzMg==',
            ]
            url = "http://1693441346.pgvv.top/yunonline/v1/wtmpdomain"
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                "Cookie": f"ejectCode=1; ysm_uid={xyy_uid}"
            }

            data = {
                "unionid": xyy_uid
            }
            for retry in range(max_retries):
                try:
                    response = requests.post(url, headers=headers, data=data, timeout=7).json()
                    break
                except (ConnectionError, Timeout):
                    if retry < max_retries - 1:
                        continue
                    else:
                        print("异常退出")
                        break
                except Exception as e:
                    print(e)
                    print("状态异常，尝试重新发送请求...")
                    response = requests.post(url, headers=headers, data=data, timeout=7).json()
            if response['errcode'] == 0:
                ukurl = response['data']['domain']
                parsed_url = urlparse(ukurl)
                query_params = parse_qs(parsed_url.query)
                uk = query_params.get('uk', [])[0] if 'uk' in query_params else None
                time.sleep(1)
                url = "https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"
                params = {
                    "uk": uk
                }
                for retry in range(max_retries):
                    try:
                        response = requests.get(url, headers=headers, params=params, timeout=7).json()
                        break
                    except (ConnectionError, Timeout):
                        if retry < max_retries - 1:
                            continue
                        else:
                            print("异常退出")
                            break
                    except Exception as e:
                        print(e)
                        print("状态异常，尝试重新发送请求...")
                        response = requests.get(url, headers=headers, params=params, timeout=7).json()
                if response['errcode'] == 0:
                    link = response['data']['link'] + "?/"
                    headers_link = {
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
                        "Cookie": f"ejectCode=1; ysm_uid={xyy_uid}"
                    }
                    response = requests.get(url=link, headers=headers_link).text
                    pattern = r'<meta\s+property="og:url"\s+content="([^"]+)"\s*/>'
                    matches = re.search(pattern, response)

                    if matches:
                        fixed_url = matches.group(1)
                        og_url = fixed_url.replace("amp;", "")

                        biz = og_url.split('__biz=')[1].split('&')[0]
                        mid = og_url.split('&mid=')[1].split('&')[0]
                        print(f"获取文章成功---{mid} 来源[{biz}]")
                        sleep = random.randint(8, 9)
                        if biz in checkDict:
                            print(f"发现目标[{biz}] 疑似检测文章！！！")
                            link = og_url
                            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

                            messages = [
                                f"出现检测文章！！！\n{link}\n请在60s内点击链接完成阅读",
                            ]

                            for message in messages:
                                data = {
                                    "msgtype": "text",
                                    "text": {
                                        "content": message
                                    }
                                }
                                headers_bot = {'Content-Type': 'application/json'}
                                response = requests.post(url, headers=headers_bot, data=json.dumps(data))
                                print("以将该文章推送至微信请在60s内点击链接完成阅读--60s后继续运行")
                                time.sleep(60)
                                url = "https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold"
                                params = {
                                    "uk": uk,
                                    "time": sleep,
                                    "timestamp": current_timestamp
                                }
                                for retry in range(max_retries):
                                    try:
                                        response = requests.get(url, headers=headers, params=params, timeout=7).json()
                                        break
                                    except (ConnectionError, Timeout):
                                        if retry < max_retries - 1:
                                            continue
                                        else:
                                            print("异常退出")
                                            break
                                    except Exception as e:
                                        print('设置状态异常')
                                        print(e)
                                if response['errcode'] == 0:
                                    gold = response['data']['gold']
                                    print(f"第{i + 1}次阅读检测文章成功---获得金币[{gold}]")
                                    print(f"{'-' * 30}")
                                else:
                                    print(f"过检测失败，请尝试重新运行")
                                    exit()
                        else:
                            print(f"本次模拟阅读{sleep}秒")
                            time.sleep(sleep)
                            url = "https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold"
                            params = {
                                "uk": uk,
                                "time": sleep,
                                "timestamp": current_timestamp
                            }
                            for retry in range(max_retries):
                                try:
                                    response = requests.get(url, headers=headers, params=params, timeout=7).json()
                                    break
                                except (ConnectionError, Timeout):
                                    if retry < max_retries - 1:
                                        continue
                                    else:
                                        print("异常退出")
                                        break
                                except Exception as e:
                                    print('设置状态异常')
                                    print(e)
                            if response['errcode'] == 0:
                                gold = response['data']['gold']
                                print(f"第{i + 1}次阅读文章成功---获得金币[{gold}]")
                                print(f"{'-' * 30}")
                            else:
                                print(f"阅读文章失败{response}")
                                break
                    else:
                        print("未找到link")

                elif response['errcode'] == 405:
                    print('阅读重复，重新尝试....')
                    print(f"{'-' * 30}")
                    time.sleep(3)
                elif response['errcode'] == 407:
                    print(f'{response}')
                    break

            else:
                print(f"获取阅读文章失败{response}")
                break

        if money_Withdrawal == 1:
            print(f"{'=' * 18}开始提现{'=' * 18}")
            url = "http://1693461882.sethlee.top/?cate=0"

            response = requests.get(url, headers=headers).text
            regex = r'request_id=([^\'"\s&]+)'
            matches = re.search(regex, response)

            request_id = matches.group(1) if matches else None

            url = 'http://1693441346.pgvv.top/yunonline/v1/gold'
            params = {
                'unionid': f'{xyy_uid}',
                'time': current_timestamp
            }
            response = requests.get(url, headers=headers, params=params).json()
            if response['errcode'] == 0:
                last_gold = response['data']['last_gold']
                gold = int(int(last_gold) / 1000) * 1000

            url = "http://1693462663.sethlee.top/yunonline/v1/user_gold"
            data = {
                "unionid": xyy_uid,
                "request_id": request_id,
                "gold": gold,
            }
            response = requests.post(url, headers=headers, data=data).json()
            print(f"当前可提现{gold}")

            url = "http://1693462663.sethlee.top/yunonline/v1/withdraw"
            data = {
                "unionid": xyy_uid,
                "signid": request_id,
                "ua": "2",
                "ptype": "0",
                "paccount": "",
                "pname": ""
            }
            response = requests.post(url, headers=headers, data=data)
            print(response.json())
        elif money_Withdrawal == 0:
            print(f"{'=' * 18}{'=' * 18}")
            print(f"不执行提现")
    else:
        print(f"获取用户信息失败")
        exit()


if __name__ == "__main__":
    accounts = os.getenv('ysm_uid')
    response = requests.get('https://gitee.com/shallow-a/qim9898/raw/master/label.txt').text
    print(response)
    if accounts is None:
        print('你没有填入ysm_uid，咋运行？')
        exit()
    else:
        accounts_list = os.environ.get('ysm_uid').split('====')
        num_of_accounts = len(accounts_list)
        print(f"获取到 {num_of_accounts} 个账号")
        with Pool(processes=num_of_accounts) as pool:
            thread_pool = ThreadPool(max_concurrency)
            thread_pool.starmap(process_account, [(account, i) for i, account in enumerate(accounts_list, start=1)])
