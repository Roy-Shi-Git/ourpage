# 我们的第 2000 天 - 纪念日网站

以「时间流淌的回忆」为主题的纪念日网站，记录你们从相识到相守的每一个珍贵瞬间。

## 功能特性

- **加载页彩蛋** - 打开网站时显示「正在加载我们的回忆...」进度条
- **实时计数器** - 首页显示「我们已经在一起 X 天」，每秒更新
- **6 大核心板块** - 封面、相遇、时间线、相册墙、心里话、结尾
- **背景音乐** - 点击爱心图标开启音乐，支持循环播放
- **滚动动画** - 元素渐显、图片轻微放大，模拟回忆浮现的感觉
- **时间线交互** - 滚动到对应位置时节点点亮
- **瀑布流相册** - 支持分类筛选，点击放大查看
- **进度指示器** - 页面顶部显示已浏览进度
- **彩蛋惊喜** - 连续点击页面左下角爱心 5 次，弹出悄悄话
- **移动端适配** - 时间线单侧排布，图片单列显示
- **打印适配** - 预留打印样式，可直接打印成实体纪念册

## 目录结构

```
ourblog/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── main.js         # 交互逻辑
├── images/
│   ├── cover/          # 封面图片
│   │   ├── cover.jpg   # 首页封面
│   │   └── recent.jpg  # 结尾近照
│   ├── timeline/       # 时间线图片（196张）
│   └── gallery/        # 相册图片（515张）
├── media/
│   └── bgm.mp3         # 背景音乐（请自行添加）
├── picture_timeline/   # 原始照片源（备份）
└── README.md
```

## 快速开始

### 1. 本地预览

```bash
# 使用 Python 简易服务器
cd /data/ourblog
python3 -m http.server 8080

# 或使用 Node.js (npx)
npx serve .

# 或使用 VS Code Live Server 扩展
```

然后访问 `http://localhost:8080`

### 2. 添加背景音乐

将你的背景音乐文件（MP3 格式）放入 `media/` 目录，命名为 `bgm.mp3`。

推荐音乐：
- 温柔抒情的纯音乐
- 对你们有特殊意义的歌曲

### 3. 自定义内容

编辑 `js/main.js` 中的配置：

```javascript
const CONFIG = {
    startDate: new Date('2021-02-12'), // 你们相识的日期
    coupleNames: ['她', '他'],
    musicVolume: 0.35,
    easterEggMessage: '你的悄悄话...'
};
```

编辑时间线内容：

```javascript
const TIMELINE_EVENTS = [
    {
        date: '2021-02-12',
        title: '初次相遇',
        description: '描述文字...',
        images: ['timeline/2021-02-12.jpg'],
        category: 'daily' // travel/daily/food/fun/festival
    },
    // 添加更多事件...
];
```

### 4. 重新处理图片

如果你的照片有更新，可以重新运行图片处理脚本：

```bash
python3 process_images.py
```

## 部署到 GitHub Pages

### 方法一：直接上传

1. 在 GitHub 创建新仓库（如 `our-2000-days`）
2. 上传所有文件到仓库
3. 进入 `Settings` → `Pages`
4. Source 选择 `Deploy from a branch`
5. Branch 选择 `main`，目录选择 `/ (root)`
6. 保存后等待几分钟
7. 访问 `https://你的用户名.github.io/仓库名/`

### 方法二：使用 Git

```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main

# 然后在 GitHub Settings 中开启 Pages
```

### 自定义域名（可选）

1. 购买域名（如 `our2000days.com`）
2. 在域名服务商添加 DNS 记录：
   - CNAME 记录指向 `你的用户名.github.io`
3. 在 GitHub Pages 设置中添加自定义域名

## 技术栈

- **HTML5 + CSS3 + Vanilla JavaScript** - 无需框架
- **AOS.js** - 滚动动画库
- **SimpleLightbox** - 图片灯箱
- **Masonry.js** - 瀑布流布局
- **Google Fonts** - 中文字体（Noto Serif SC、Ma Shan Zheng）

## 浏览器兼容性

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 自定义样式

在 `css/style.css` 中修改 CSS 变量：

```css
:root {
    /* 配色方案 */
    --color-bg-primary: #FDF8F3;    /* 米白背景 */
    --color-accent-primary: #D4A5A5; /* 豆沙粉 */
    --color-accent-tertiary: #C9959A;/* 深豆沙 */
    
    /* 字体 */
    --font-serif: 'Noto Serif SC';   /* 标题字体 */
    --font-handwriting: 'Ma Shan Zheng'; /* 手写字体 */
}
```

## 性能优化

- 图片已压缩至 1920px 宽度
- 使用 WebP/JPEG 格式
- 支持原生懒加载 `loading="lazy"`
- CSS 动画使用 GPU 加速

## 常见问题

### Q: 音乐无法播放？
A: 现代浏览器禁止自动播放音频，必须用户点击播放按钮。可以使用 MP3 格式，确保文件可访问。

### Q: 图片显示为占位符？
A: 检查 `images/timeline/` 和 `images/gallery/` 目录是否有图片文件。

### Q: 动画不流畅？
A: 移动设备上可以关闭部分动画，编辑 `js/main.js` 中的 AOS 配置。

## License

MIT License - 仅供参考学习使用

---

*Made with ❤️ for our 2000 days*
