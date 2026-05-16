---
name: productivity-tools
description: "效率工具 — PPT/OCR 文档/地图。Trigger: PPT/OCR/地图. Do NOT trigger for 飞书文档操作。"
version: 1.1.0
---
# 效率工具

## 一句话版本
集成 PowerPoint 创建/编辑、PDF/扫描件 OCR、地图定位/导航等效率工具能力。

## 触发条件
- ✅ **触发**：PPT 创建/编辑、PDF/扫描件 OCR 识别、地图定位/路线查询、文档格式转换
- ❌ **不触发**：飞书文档操作（用 lark-cli）、代码编辑、纯文本处理

## 核心能力

### 1. PowerPoint 创建/编辑
- 创建新 PPT 文件（支持自定义模板）
- 编辑现有 PPT（添加/修改幻灯片、文本、图片、图表）
- 导出为 PDF/图片

```python
# 使用 python-pptx 创建 PPT
from pptx import Presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "标题"
prs.save("output.pptx")
```

### 2. OCR 文档识别
- PDF/扫描件文字提取
- 支持中文/英文/多语言
- 输出可编辑文本或结构化数据

```bash
# 使用 Tesseract OCR
tesseract input.png output -l chi_sim+eng

# 使用 PaddleOCR（中文效果更佳）
paddleocr --image_dir input.png --lang ch
```

### 3. 地图定位/导航
- 地址解析（地址 → 经纬度）
- 路线规划（驾车/步行/公交）
- 周边搜索（POI 查询）

```python
# 使用高德/百度地图 API
import requests
response = requests.get("https://restapi.amap.com/v3/geocode/geo", params={
    "key": "YOUR_KEY",
    "address": "北京市朝阳区"
})
```

## 工作流
1. **识别任务类型**：PPT / OCR / 地图
2. **选择对应工具链**：python-pptx / Tesseract(PaddleOCR) / 地图 API
3. **准备输入**：文件路径/URL/参数
4. **执行处理**：调用工具
5. **输出结果**：文件/文本/坐标

## 异常处理

### PPT 生成失败
- **症状**：python-pptx 报错、模板不兼容、保存失败
- **排查**：检查模板文件是否损坏、路径是否正确、权限是否足够
- **恢复**：使用默认模板、检查文件路径、验证写入权限

### OCR 识别率低
- **症状**：识别结果乱码、大量遗漏
- **排查**：图片清晰度、语言包是否安装、文档是否倾斜
- **恢复**：预处理图片（增强对比度/旋转校正）、更换 OCR 引擎（Tesseract → PaddleOCR）

### 地图 API 调用失败
- **症状**：返回空结果、坐标错误、API 报错
- **排查**：API Key 是否有效、地址格式是否正确、网络是否通畅
- **恢复**：更换地图服务（高德 ↔ 百度）、检查 Key 配额

### 文件过大处理失败
- **症状**：内存不足、处理超时
- **排查**：文件大小、系统资源限制
- **恢复**：分块处理、压缩文件、使用流式处理

## 常见坑点
- ⚠️ python-pptx 不支持所有 PPT 特性（如复杂动画、嵌入视频）
- ⚠️ Tesseract 对中文识别效果一般，推荐 PaddleOCR 作为主力
- ⚠️ OCR 处理扫描 PDF 需先转换为图片（使用 pdf2image）
- ⚠️ 地图 API 有日调用限额，需监控使用量
- ⚠️ 批量 PPT 生成注意内存管理，处理完及时释放对象
