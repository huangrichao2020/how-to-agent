---
name: segment-anything-model
description: Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image.
version: 1.1.0
author: Orchestra Research
license: MIT
dependencies: [segment-anything, transformers>=4.30.0, torch>=1.7.0]
metadata:
  hermes:
    tags: [Multimodal, Image Segmentation, Computer Vision, SAM, Zero-Shot]

---

# Segment Anything Model (SAM)

Meta AI's zero-shot image segmentation foundation model. Segments any object in any image using point, box, or mask prompts — no task-specific training required.

**Trained on:** 1.1 billion masks from 11 million images (SA-1B dataset)

## 快速决策：要不要用 SAM？

| 你的需求 | 推荐方案 |
|---|---|
| 交互式分割（点击标注物体） | ✅ SAM |
| 自动提取图像中所有物体 | ✅ SAM (AutomaticMaskGenerator) |
| 按文字描述分割物体 | ❌ 用 GroundingDINO + SAM |
| 实时目标检测（带分类） | ❌ 用 YOLO |
| 视频分割 | ❌ 用 SAM 2 |
| 语义/全景分割（带类别标签） | ❌ 用 Mask2Former |

## 安装与模型选择

### 安装
```bash
# 方式 1: 官方 GitHub（推荐）
pip install git+https://github.com/facebookresearch/segment-anything.git

# 方式 2: HuggingFace Transformers
pip install transformers

# 可选依赖
pip install opencv-python pycocotools matplotlib onnx onnxruntime
```

### 模型选择指南
| 模型 | 权重 | 速度 | 精度 | 最低显存 | 推荐场景 |
|---|---|---|---|---|---|
| ViT-B | 375 MB | 最快 | 良 | 2 GB | 日常使用、资源受限 |
| ViT-L | 1.2 GB | 中等 | 好 | 4 GB | 质量与速度平衡 |
| ViT-H | 2.4 GB | 最慢 | 最佳 | 8 GB | 追求最高精度 |

```bash
# 下载权重（选一个即可）
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth  # ViT-H
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth  # ViT-L
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth  # ViT-B
```

## 核心架构

```
SAM 三阶段流水线：
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │
│     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                       │                       │
  Image Embeddings      Prompt Embeddings         Masks + IoU
  (计算一次)            (每次提示)                predictions
```

**关键设计：** Image Embeddings 只需计算一次，后续可以反复用不同的 prompt 快速查询。

## 快速开始

### 方式 1: 官方 API（SamPredictor）

```python
import numpy as np, cv2
from segment_anything import sam_model_registry, SamPredictor

# 加载模型 + 创建预测器
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
sam.to(device="cuda")
predictor = SamPredictor(sam)

# 设置图像（计算 embeddings，只需一次）
image = cv2.cvtColor(cv2.imread("image.jpg"), cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# 点提示分割
masks, scores, _ = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),       # 1=前景, 0=背景
    multimask_output=True             # 返回 3 个候选
)
best_mask = masks[np.argmax(scores)]  # 取最佳
```

### 方式 2: HuggingFace Transformers

```python
from transformers import SamModel, SamProcessor
from PIL import Image

model = SamModel.from_pretrained("facebook/sam-vit-huge")
processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")
model.to("cuda")

inputs = processor(Image.open("image.jpg"), input_points=[[[450, 600]]], return_tensors="pt")
inputs = {k: v.to("cuda") for k, v in inputs.items()}
masks = processor.image_processor.post_process_masks(
    model(**inputs).pred_masks.cpu(),
    inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu()
)
```

## 提示类型详解

| 提示类型 | 用法 | 适用场景 |
|---|---|---|
| 前景点 | `point_labels=[1]` | 点击选中单个物体 |
| 背景点 | `point_labels=[0]` | 排除不需要的区域 |
| 组合点 | `[1,1,0]` 混合 | 精确控制分割边界 |
| 边界框 | `box=[x1,y1,x2,y2]` | 大物体、已知范围 |
| 框+点 | 两者同时传入 | 最高精度控制 |
| 历史掩码 | `mask_input=prev_mask` | 迭代 refinement |

```python
# 组合提示示例：框 + 前景点 + 背景点
masks, scores, _ = predictor.predict(
    point_coords=np.array([[500, 375], [600, 400]]),
    point_labels=np.array([1, 0]),          # 前景 + 背景
    box=np.array([400, 300, 700, 600]),      # 约束范围
    multimask_output=False
)

# 迭代 refinement：用上一次的最佳掩码作为输入
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375], [550, 400]]),
    point_labels=np.array([1, 0]),
    mask_input=logits[np.argmax(scores)][None, :, :],
    multimask_output=False
)
```

## 自动分割（无提示）

```python
from segment_anything import SamAutomaticMaskGenerator

# 默认配置
mask_generator = SamAutomaticMaskGenerator(sam)
masks = mask_generator.generate(image)

# 自定义参数（调优方向）
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,               # ↑ 更多掩码, ↓ 更快
    pred_iou_thresh=0.88,             # ↑ 更严格的质量过滤
    stability_score_thresh=0.95,      # ↑ 过滤边缘模糊的掩码
    crop_n_layers=1,                  # 多尺度裁剪检测
    min_mask_region_area=100,         # 过滤微小掩码
)

# 过滤结果
masks = sorted(masks, key=lambda x: x['area'], reverse=True)  # 按面积排序
high_quality = [m for m in masks if m['predicted_iou'] > 0.9]
```

**每个掩码的字段：** `segmentation`(二值图), `bbox`, `area`, `predicted_iou`(质量分), `stability_score`(鲁棒性分), `point_coords`(生成点)

## 常用工作流

### 1. 物体提取（透明背景）
```python
def extract_object(image, point):
    predictor.set_image(image)
    masks, scores, _ = predictor.predict(
        point_coords=np.array([point]), point_labels=np.array([1]), multimask_output=True)
    best_mask = masks[np.argmax(scores)]
    rgba = np.zeros((*image.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = image
    rgba[:, :, 3] = best_mask * 255
    return rgba
```

### 2. 医学图像（灰度转 RGB）
```python
medical = cv2.cvtColor(cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2RGB)
predictor.set_image(medical)
masks, scores, _ = predictor.predict(box=np.array([x1, y1, x2, y2]), multimask_output=True)
```

### 3. COCO RLE 编码（用于数据集标注）
```python
from pycocotools import mask as mask_utils
rle = mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))
rle["counts"] = rle["counts"].decode("utf-8")
```

## 性能优化

| 优化方向 | 方法 |
|---|---|
| 显存不足 | 换 ViT-B，或 `torch.cuda.empty_cache()` 清理缓存 |
| 推理慢 | 用 ViT-B，`points_per_side` 降到 16，开启半精度 `sam.half()` |
| 大批量 | embeddings 计算一次后复用不同 prompts |
| 部署 | 导出 ONNX：`python scripts/export_onnx_model.py --checkpoint ... --return-single-mask` |
| 大图像 | SAM 自动缩放到 1024×1024，无需预处理 |

## 异常处理与故障排查

### 预检脚本
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
python -c "import segment_anything; print('SAM OK')"
ls -lh sam_vit_*.pth  # 检查权重文件
```

### 常见问题速查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| OOM | 模型太大/显存不足 | 换 ViT-B 或 `torch.cuda.empty_cache()` |
| 推理慢 | 大模型或多提示 | ViT-B + 减少 `points_per_side` + 半精度 |
| 掩码质量差 | 提示不够/有歧义 | 用 box+点组合；用 iterative refinement |
| 边缘锯齿 | 掩码边界模糊 | `stability_score_thresh` 提高到 0.95 |
| 小物体漏检 | 网格太稀疏 | `points_per_side` 升到 64 |
| 权重下载失败 | 网络/防火墙 | 换镜像源或手动下载，校验 checksum |
| 无 GPU | 无显卡或驱动问题 | CPU 可跑 ViT-B，但慢 10-50x |
| 导入失败 | 包版本不对 | `pip install git+https://github.com/facebookresearch/segment-anything.git` |

### 回退策略
- **无 GPU** → ViT-B on CPU（可用但慢）
- **SAM 1 做不了视频** → 升级到 SAM 2
- **需要文字驱动分割** → GroundingDINO + SAM 组合

## 参考资源

- **GitHub**: https://github.com/facebookresearch/segment-anything
- **论文**: https://arxiv.org/abs/2304.02643
- **在线 Demo**: https://segment-anything.com
- **SAM 2（视频）**: https://github.com/facebookresearch/segment-anything-2
- **HuggingFace**: https://huggingface.co/facebook/sam-vit-huge
