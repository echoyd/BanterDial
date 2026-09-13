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

三个档位都会根据用户语言调整表达。简体中文不再照搬英文段子结构：Grounded 更像自然的中文工程交流，Weird 只加一次轻微反转，Unhinged 使用更本土的反差、一本正经胡说和生活化比喻，并在包袱落地后及时闭嘴。

遇到安全、隐私、生产事故等高风险内容时会暂时回到 Grounded；话题结束后自动恢复此前选择的档位。

## 额度与隐私

BanterDial 只在明确输入 `$banter-dial` 时启用。它没有后台进程、账号、网络请求、MCP 服务或外部工具；普通切换只加载精简主说明，默认保持短回答。OpenAI 没有公布一次 Skill 调用对应多少额度百分比，因此项目不编造固定数字。

普通使用不需要 Python。只有校验或渲染 Banter Card 时才需要 Python 3.11+。

许可证：MIT。
