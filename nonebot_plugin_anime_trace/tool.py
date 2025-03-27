import ssl


def ntqq_ssl_context() -> ssl.SSLContext:
    """创建符合 QQ 服务器要求的 ssl 上下文

    Returns:
        ssl.SSLContext: ssl 上下文
    """
    ssl_context = ssl.create_default_context()  # 创建 SSL 兼容上下文，适配 QQ 服务器
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
    )  # 关闭不兼容的 TLS 版本
    ssl_context.set_ciphers("HIGH:!aNULL:!MD5")  # 只允许高强度加密
    return ssl_context
