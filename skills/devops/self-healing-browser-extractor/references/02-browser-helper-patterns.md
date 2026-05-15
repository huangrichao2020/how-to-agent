# browser_helper.py 常用模式

## 模式 1: 动态内容不渲染
SPA 页面 headless 下不渲染，等待特定元素出现
```python
def wait_for_element(selector, timeout=10):
    import time
    end = time.time() + timeout
    while time.time() < end:
        if page.query_selector(selector):
            return True
        time.sleep(0.5)
    return False
```

## 模式 2: 反爬弹窗拦截
访问后弹出登录/验证，注入 CSS 隐藏
```python
def bypass_popup(page):
    page.evaluate("""
        document.querySelectorAll('.popup, .modal, .overlay')
            .forEach(el => el.remove())
    """)
```

## 模式 3: Cookie 复用
```python
def save_cookies(page, path):
    import json
    cookies = page.context.cookies()
    with open(path, 'w') as f:
        json.dump(cookies, f)

def load_cookies(page, path):
    import json, os
    if os.path.exists(path):
        with open(path) as f:
            page.context.add_cookies(json.load(f))
```

## 模式 4: 微信公众号文章提取
绕过验证码，正则提取 rich_media_content 区域
```python
def extract_wechat_article(url):
    # 微信文章提取专用函数
    pass
```

## 模式 5: AJAX 加载等待
```python
def wait_for_ajax(page, timeout=10):
    return page.evaluate("""
        () => new Promise(resolve => {
            setTimeout(resolve, 1000)
        })
    """)
```
