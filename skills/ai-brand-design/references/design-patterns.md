# HTML/CSS 设计模式库

源自 huashu-design 的核心技术实现。所有模式均为纯 CSS，零依赖。

---

## 1. 色彩模式

### HSL 色相驱动（换品牌色只改一个值）
```css
:root {
  --brand-hue: 22;  /* 橙色 → 改 220 变蓝色 */
  --brand-500: hsl(var(--brand-hue), 85%, 55%);
  --brand-surface: hsl(var(--brand-hue), 20%, 96%);
  --brand-text: hsl(var(--brand-hue), 25%, 15%);
}
```

### 渐变背景
```css
.hero-bg {
  background:
    radial-gradient(ellipse at 20% 50%,
      hsla(var(--brand-hue), 80%, 70%, 0.12) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%,
      hsla(calc(var(--brand-hue) + 40), 70%, 60%, 0.08) 0%, transparent 50%),
    var(--brand-surface);
}
```

### 毛玻璃效果
```css
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}
```

---

## 2. 布局模式

### 12 列 Grid
```css
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-4);
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-4);
}
.span-8 { grid-column: 1 / 9; }
.span-4 { grid-column: 9 / 13; }

@media (max-width: 768px) {
  .span-8, .span-4 { grid-column: 1 / -1; }
}
```

### 响应式 Flex 卡片
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-6);
}
```

### 粘性导航
```css
.sticky-nav {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
}
```

---

## 3. 装饰模式

### 圆点图案
```css
.dot-pattern {
  background-image: radial-gradient(
    circle, var(--brand-primary) 1px, transparent 1px
  );
  background-size: 24px 24px;
  opacity: 0.08;
}
```

### 渐变边框
```css
.gradient-border {
  position: relative;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}
.gradient-border::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--brand-400), var(--brand-600));
  z-index: -1;
}
```

### Blob 有机形状
```css
.blob {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  animation: blob-morph 8s ease-in-out infinite;
}
@keyframes blob-morph {
  0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
}
```

### 对角线分割
```css
.diagonal-section {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}
```

---

## 4. 动画模式

### 渐入上移
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-up {
  animation: fade-up 0.6s var(--transition-base) both;
}
```

### 交错子元素
```css
.stagger-children > * {
  animation: fade-up 0.5s ease both;
}
.stagger-children > *:nth-child(1) { animation-delay: 0.1s; }
.stagger-children > *:nth-child(2) { animation-delay: 0.2s; }
.stagger-children > *:nth-child(3) { animation-delay: 0.3s; }
.stagger-children > *:nth-child(4) { animation-delay: 0.4s; }
```

### Hover 上浮
```css
.card {
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

### 减少动效兼容
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 5. 组件模式

### 按钮
```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-semibold);
  text-decoration: none;
  transition: all var(--transition-fast);
  cursor: pointer;
  border: none;
  font-size: var(--text-base);
}
.btn-primary {
  background: var(--brand-500);
  color: white;
}
.btn-primary:hover {
  background: var(--brand-600);
  transform: translateY(-1px);
}
.btn-secondary {
  background: transparent;
  color: var(--brand-600);
  border: 2px solid var(--brand-500);
}
```

### 标签/Tag
```css
.tag {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: hsl(var(--brand-hue), 80%, 92%);
  color: hsl(var(--brand-hue), 80%, 35%);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}
```

### 头像
```css
.avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--brand-400), var(--brand-600));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-bold);
  font-size: var(--text-lg);
}
```

### 引用块
```css
.blockquote {
  border-left: 4px solid var(--brand-500);
  padding: var(--space-4) var(--space-6);
  margin: var(--space-6) 0;
  background: hsl(var(--brand-hue), 80%, 97%);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
```

---

## 6. 暗色模式

```css
@media (prefers-color-scheme: dark) {
  :root {
    --brand-surface: hsl(var(--brand-hue), 20%, 10%);
    --brand-text: hsl(var(--brand-hue), 15%, 92%);
    --color-border: hsl(var(--brand-hue), 15%, 25%);
    --brand-500: hsl(var(--brand-hue), 70%, 60%);
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
  }
}
```

---

## 快速参考：常用 CSS 速查

| 需求 | 方案 |
|------|------|
| 换品牌色 | 改 `--brand-hue` |
| 响应式 | `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` |
| 垂直居中 | `display: grid; place-items: center;` |
| 文字截断 | `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;` |
| 图片铺满 | `object-fit: cover; width: 100%; height: 100%;` |
| 固定宽高比 | `aspect-ratio: 16 / 9;` |
| 文字渐变 | `background: linear-gradient(...); -webkit-background-clip: text; -webkit-text-fill-color: transparent;` |
