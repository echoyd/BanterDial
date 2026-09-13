# BanterDial 中文说明

**一条命令，三种话风，严谨度不变。**

[English](README.md)

![Grounded、Weird 与 Unhinged 对比](plugins/banter-dial/assets/mode-comparison.png)

## 最简单的安装方式

把下面这句话粘贴进 Codex：

```text
$skill-installer Install banter-dial from https://github.com/echoyd/BanterDial/tree/main/plugins/banter-dial/skills/banter-dial
```

如果没有立即出现，重启一次 Codex。

也可以通过 Plugin 安装：

```bash
codex plugin marketplace add echoyd/BanterDial --ref main
codex plugin add banter-dial@banterdial
```

## 使用

```text
$banter-dial
```

默认直接进入 Weird，不弹菜单、不要求配置。

```text
$banter-dial grounded
$banter-dial weird
$banter-dial unhinged
$banter-dial off
```

- Grounded：正常、清楚、简短。
- Weird：有点抽象，但一眼能懂。
- Unhinged：明显发疯，事实和代码仍然正常。

## 额度与隐私

BanterDial 只在明确输入 `$banter-dial` 时启用。它没有后台进程、账号、网络请求、MCP 服务或外部工具；普通切换只加载精简主说明，默认保持短回答。OpenAI 没有公布一次 Skill 调用对应多少额度百分比，因此项目不编造固定数字。

普通使用不需要 Python。只有校验或渲染 Banter Card 时才需要 Python 3.11+。

许可证：MIT。
