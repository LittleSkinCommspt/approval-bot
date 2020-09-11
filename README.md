# LittleSkin 入群审核机器人
迁移至 mirai！

---

## 部署
1. 克隆此仓库
2. 设置 `graia-host`、`graia-authkey` 和 `graia-account` 这三个环境变量。第一个为 `mirai-http-api` 地址，第二个为 `authkey`，第三个为机器人的 QQ 号。你可以在 `mirai-http-api` 的配置文件（`plugins/MiraiAPIHTTP/setting.yml`）中找到前两项。
3. 确保配置文件中的 `enableWebsocket` 被设置为 `true`
4. 确保你安装了 Python3.6 +
5. 使用恰当的方法安装依赖，如 `pip3 install -r requirements.txt`
6. 使用恰当的 Python3 版本运行 `main.py`，机器人开始运行
