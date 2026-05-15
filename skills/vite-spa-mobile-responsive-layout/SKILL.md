---
name: vite-spa-mobile-responsive-layout
description: 为 Vite + React SPA 添加移动端响应式布局适配。核心：检测屏幕宽度，切换桌面端三栏（侧边栏+内容+助手）为移动端顶栏+内容+底栏布局。
category: frontend
yao_category: "其他"
---

## 适用场景
- Vite + React + TypeScript 项目需要适配手机/平板端
- 桌面端有固定侧边栏或右侧面板，移动端需要改为顶部/底部导航
- 使用 inline styles 或 CSS-in-JS，而非纯 CSS media queries

## 实施步骤

### 1. 创建响应式检测 Hook/State
在主布局组件（如 `AppShell.tsx`）中添加窗口宽度检测：

```tsx
const [isMobile, setIsMobile] = useState(false)

useEffect(() => {
  const check = () => setIsMobile(window.innerWidth < 768)
  check()
  window.addEventListener('resize', check)
  return () => window.removeEventListener('resize', check)
}, [])
```

### 2. 拆分移动端专用组件
将导航和助手面板拆分为移动端简化版：

**MobileTopNav.tsx**（顶部水平滚动导航）：
- 使用 `position: fixed; top: 0; left: 0; right: 0`
- 分组标签横向滚动 → 点击展开具体选项芯片
- 高度约 70px，预留 `marginTop` 给内容区

**MobileAssistant.tsx**（底部助手入口）：
- 默认显示「💬 复盘大师」按钮条（`position: fixed; bottom: 0`）
- 点击后弹出 55vh 高度的全屏助手面板
- 带关闭按钮，收起回到底部按钮条

### 3. 主布局条件渲染
```tsx
if (isMobile) {
  return (
    <>
      <MobileTopNav />
      <div style={{ marginTop: 70, marginBottom: 44, overflowY: 'auto' }}>
        {/* 内容区 */}
      </div>
      <MobileAssistant />
    </>
  )
}

// 桌面端原有三栏布局
return (
  <div style={{ display: 'flex', height: '100vh' }}>
    <Sidebar />
    <MainContent />
    <AssistantPanel />
  </div>
)
```

### 4. 关键样式要点
- **移动端内容区**：`marginTop` = 顶栏高度，`marginBottom` = 底栏高度
- **固定定位元素**：`zIndex` 设为 60+，确保高于内容区
- **滚动隔离**：内容区 `overflowY: auto`，避免整体页面滚动
- **触摸优化**：按钮最小点击区域 44x44px，字体不小于 0.68em

### 5. 构建与部署
```bash
npm run build
cp -r dist/* /path/to/nginx/root/
```

## 常见陷阱
1. **Resize 事件泄漏**：务必在 `useEffect`  cleanup 中移除监听器
2. **SSR 不匹配**：如果项目支持 SSR，初始 `isMobile` 应基于 user-agent 或服务端判断，避免 hydration mismatch
3. **横屏切换**：部分平板横屏时宽度 > 768px 但仍是触控交互，可根据需求调整阈值或使用 `pointer: coarse` media query
4. **虚拟键盘弹起**：移动端输入框聚焦时虚拟键盘可能遮挡底部按钮，需监听 `visualViewport` 变化或增加 `paddingBottom`

## 参考实现
见 `/root/info-hub/frontend/src/components/layout/AppShell.tsx` 中的 `MobileTopNav` 和 `MobileAssistant` 组件。