# 简道云 Webhook 接收演示

此项目包含各语言环境下，接受简道云 Webhook 回调请求并验证签名的简单演示工程。默认服务端启动在 `3100` 端口，签名使用的默认密钥为 `test-secert`。

## 签名验证流程

1. 为了防止 webhook 接收接口被第三方恶意攻击，用户在开发回调接口时，建议对回调请求进行签名校验，以确保回调请求来源来自于简道云。
2. 获取 POST 请求体 body 内容，序列化为计算签名使用的 payload
3. 获取请求参数中的nonce和timestamp
4. 将 payload 与签名密钥 secret 按照 "\<nonce>:\<payload>:\<secret>:\<timestamp>" 的形式组合为校验字符串 content
5. 以 utf-8 编码形式计算 content 的 sha-1 散列
6. 将 content 散列的十六进制字符串与 POST 请求 header 中的 'X-JDY-Signature' 做比较
7. 若比较结果相同，则通过签名验证；若比较结果不同，则无法通过检查

演示工程使用 flask 框架，经过 Python 3.x 环境测试。

使用前首先安装相关依赖(推荐使用 virtualenv 配置测试环境)：

```bash
pip install -r requirements.txt
```

启动运行

```bash
python ./server.py
```

## 