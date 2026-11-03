# 网页数据复建源

R04-web-build.py只复制本轮已审核媒体/源文件、生成review-data.json与PUBLIC_MANIFEST.json，不生成游戏代码，不制作压缩包，不推送或发布。

在已有网页检出目录中执行：

```bash
python3 sources/r04/web/R04-web-build.py --source /path/to/R04-review-inputs --repo .
```

输入根必须包含DECISIONS.json/md、characters/、audio/、ui/，目录结构与保留的sources/r04一致。HTML、app.js和style.css是仓库中的普通可编辑源，不由此脚本重画。默认路径仅对应本轮实际云环境/workspace/shared/R04-review与/workspace/ball_art_review，可用参数替换。

脚本不删除旧文件、不给缺失新音频回退旧R03音频。每次最终QA报告写完后重建一次manifest，随后不要再改被清单覆盖的文件。
