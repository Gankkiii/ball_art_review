# R05 评审网页复建

`python web/R05-web-build.py --source /path/to/R05-ui-review --repo /path/to/ball_art_review`

输入可用本目录上一级的完整 sources/r05 树；生成公开数据和资产白名单及哈希清单，不发布、不删除历史、不改游戏。HTML/CSS/JS为仓库docs/index.html、docs/r05中的普通静态源码；builder不改它们。页面默认浏览第一张仅为展示顺序，选择框保持未选。禁止将浏览或生成草稿视为用户批准。
