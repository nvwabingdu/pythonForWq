
# 暂未完成
import os
import re
import base64
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.edge.options import Options  # 改成 Edge
from selenium.webdriver.common.by import By
import requests

# =================配置=================
GOODS_URL = "https://item.jd.com/100140999186.html"
DESKTOP = os.path.expanduser("~/Desktop")
SAVE_FOLDER = os.path.join(DESKTOP, "京东商品")
IMG_FOLDER = os.path.join(SAVE_FOLDER, "全部商品图片")
PDF_PATH = os.path.join(SAVE_FOLDER, "商品完整详情.pdf")
os.makedirs(SAVE_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

# ========== 浏览器配置：改为 Edge ==========
opt = Options()
opt.add_argument("--headless=new")  # 后台运行不弹窗
opt.add_argument("--disable-gpu")
opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# 启动 Edge 浏览器（自动匹配系统自带的 Edge）
driver = webdriver.Edge(options=opt)
driver.get(GOODS_URL)

# 滚动到底部触发全部懒加载图片
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)
html_raw = driver.page_source
headers = {"User-Agent": driver.execute_script("return navigator.userAgent")}

# 1、下载页面css/js/小资源，用于离线html
def down_file(res_url):
    try:
        full_url = urljoin(GOODS_URL, res_url)
        fname = os.path.basename(full_url.split("?")[0])
        if not fname: fname = f"res_{hash(full_url)}"
        save_p = os.path.join(SAVE_FOLDER, fname)
        if os.path.exists(save_p): return fname
        cont = requests.get(full_url, headers=headers, timeout=8).content
        with open(save_p, "wb") as f: f.write(cont)
        return fname
    except: return res_url

# 2、单独下载所有高清商品图（主图+详情大图）
img_idx = 1
def down_detail_img(img_url, idx):
    try:
        full_url = urljoin(GOODS_URL, img_url)
        suffix = full_url.split(".")[-1].split("?")[0]
        if suffix not in ["jpg","jpeg","png","avif","webp"]: suffix = "jpg"
        save_name = f"详情图_{idx}.{suffix}"
        save_path = os.path.join(IMG_FOLDER, save_name)
        if os.path.exists(save_path): return
        pic = requests.get(full_url, headers=headers, timeout=10).content
        with open(save_path, "wb") as f: f.write(pic)
        print(f"已保存图片：{save_name}")
    except Exception: pass

# 抓取全部图片真实地址（优先data-origin/data-src高清原图）
# 预览主图
pre_imgs = driver.find_elements(By.CSS_SELECTOR, "div.preview img")
for img in pre_imgs:
    src = img.get_attribute("data-origin") or img.get_attribute("src")
    if src:
        down_detail_img(src, img_idx)
        img_idx += 1
# 详情所有图片
all_img = driver.find_elements(By.TAG_NAME, "img")
for img in all_img:
    src = img.get_attribute("data-src") or img.get_attribute("data-original") or img.get_attribute("data-lazy") or img.get_attribute("src")
    if src and (src.startswith("/") or "jd.com" in src) and not src.endswith(".gif"):
        down_detail_img(src, img_idx)
        img_idx += 1

# 替换资源路径，生成离线html
html_raw = re.sub(r'src="([^"]+)"', lambda x: f'src="{down_file(x.group(1))}"', html_raw)
html_raw = re.sub(r'href="([^"]+\.(css|js))"', lambda x: f'href="{down_file(x.group(1))}"', html_raw)
html_save = os.path.join(SAVE_FOLDER, "离线完整网页.html")
with open(html_save, "w", encoding="utf-8") as f: f.write(html_raw)

# ==========生成PDF【关键：CDP导出完整整页PDF，保留图片文字背景】==========
pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
    "landscape": False,
    "format": "A4",
    "printBackground": True,      # 保留图片、背景样式
    "preferCSSPageSize": True,
    "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,
    "scale": 0.95
})
with open(PDF_PATH, "wb") as f:
    f.write(base64.b64decode(pdf_data["data"]))

driver.quit()

# 输出结果
print("\n=====保存完成，桌面【京东商品】文件夹=====")
print(f"1.完整PDF文档：{os.path.basename(PDF_PATH)}（全部图文排版）")
print(f"2.离线网页：离线完整网页.html（断网可打开）")
print(f"3.全部原图目录：{IMG_FOLDER}，总计{img_idx-1}张")