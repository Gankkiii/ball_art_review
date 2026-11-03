# 用户评审包 · R01 · A/B/C v1.0 · 包修订1.1

三个方案均待用户选择。先看 balls_art_round1.pdf，再播放 motion/demo_A.mp4，或打开 balls_art_round1.pptx。PPT由总负责人整合，章节涵盖方案、比较、推荐和下周期选项。第13页嵌入带声音MP4，独立MP4作为手机备用；六条WAV与试听页位于audio。当前python-pptx无本轮已验证的原生音频插入接口，未伪装音频为视频；采用PPT包内相对链接及独立文件备用。请解压完整ZIP并保留目录结构。

PDF是静态阅读版，视频页只显示已有画面，不播放；音视频请打开独立文件。PPT本身无需网络获得嵌入视频，但PowerPoint/WPS内播放兼容性尚未实际验证。

index.html为入口，motion/index.html支持三方向切换。手机文件管理器可能不支持本地HTML资源；优先PDF与MP4。桌面可在此目录运行 python -m http.server 8000 --bind 127.0.0.1，然后打开 http://127.0.0.1:8000/ 。没有外部发布。

画面与音频未重新设计；本次仅整理版本、媒体嵌入和打包。来源授权见SOURCES_LICENSES.md；每个文件的版本与实际验证状态见manifest.json及qa/REPORT.md。全方案待选择；本包不表示已批准接入。手机窄屏HUD较小；Godot、Android真机、人工听审未运行。

点点接入包单独提供。用户选定方向并明确批准后才交点点接入。不会自动启动下周期。
