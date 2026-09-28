"""Workbook 4's PDF conversion mini-task; rendered by the course builder."""

INSTALL_COMMANDS = """cd /workspaces/AI_workshop
. .venv/bin/activate
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
cd /workspaces/AI_workshop"""

CONVERT_COMMANDS = """cd /workspaces/AI_workshop
. .venv/bin/activate
mkdir -p _for_STUDENT/outputs/04_debugging_and_extensions
markitdown "_for_STUDENT/data/notebook4/pipeline_overview_sample.pdf" > _for_STUDENT/outputs/04_debugging_and_extensions/pipeline_overview_sample.md"""

AGENT_PROMPT = """Convert _for_STUDENT/data/notebook4/pipeline_overview_sample.pdf into Markdown.
Save it as _for_STUDENT/outputs/04_debugging_and_extensions/pipeline_overview_sample.agent.md.
Preserve the wording, headings, lists, numbers and reading order as faithfully as possible.
Represent tables as Markdown tables where possible. Describe diagrams only if you can inspect them;
flag content you cannot read instead of inventing it. Do not summarise or add new claims.
For this comparison, do not use MarkItDown or read the other conversion's output.
Use the original PDF as your source. Tell me which tools you used and any limitations.
If you cannot access the PDF, say so and ask for an accessible attachment; do not guess its contents."""


def extensions_lesson_cells(markdown, code):
    def prompt(text, title, destination="chat"):
        return code(
            f"copyable_prompt({text!r}, title={title!r}, destination={destination!r})",
            "interactive",
        )

    return [
        markdown("""
### Experiment 5C · Mini-task: one PDF, two conversions

Agents can help convert file formats as well as debug code. Turn the same PDF
into two Markdown files, then compare both against the original. Markdown
(`.md`) is a plain-text format with headings, lists and other lightweight markup.

Open the permanent exercise copy:
[pipeline_overview_sample.pdf](../data/notebook4/pipeline_overview_sample.pdf).
You will find both outputs in **_for_STUDENT → outputs → 04_debugging_and_extensions**.
"""),
        markdown("""
### What is MCP?

**Model Context Protocol (MCP)** is a standard way for an AI agent to connect to
external tools and data. An MCP server makes capabilities available to the
agent—for example, converting a document—so it can use the result in a larger workflow.

Microsoft's **MarkItDown** converts files to Markdown. Its MCP server exposes
that converter to an agent; normal PDF conversion does **not** use a built-in
LLM. Optional LLM features require separate configuration. You choose the chat
model; an agent can also delegate to another model when its tools support that.

Sources: [Microsoft MarkItDown](https://github.com/microsoft/markitdown) ·
[Microsoft's MCP server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp).
"""),
        markdown("""
### A · Install MarkItDown and convert in the terminal

Run the next cell to display **Copy commands**, then paste its contents into the
**terminal** and press Enter. The commands activate the workshop environment and
install Microsoft's command-line converter. They are not Python notebook code.
Use your actual workspace path if it differs from `/workspaces/AI_workshop`.
If you already cloned `markitdown`, skip the `git clone` line and reuse that folder.
Installation can take a few minutes.
"""),
        prompt(INSTALL_COMMANDS, "Install MarkItDown · Copy into the terminal", "terminal"),
        markdown("""
In the terminal, type `markitdown`, add the quoted PDF path, then use `>` followed
by the output path. You can right-click the PDF in Explorer and **Copy Path**.
The complete command is provided below; rerunning it replaces that output file.
"""),
        prompt(CONVERT_COMMANDS, "Convert the PDF · Copy into the terminal", "terminal"),
        markdown("""
Find **pipeline_overview_sample.md** in the output folder and open it. Check that
it contains text, then compare its headings and reading order with the PDF.
An empty file may mean conversion failed: read the terminal error first.

<details>
<summary><b>Use the MarkItDown MCP server through the agent instead</b></summary>

This is an alternative way to call the converter. Installing the MCP server in
VS Code is separate from installing the `markitdown` terminal command.

1. Open **Extensions**, enable MCP servers if your interface prompts you, and
   search **@mcp markitdown**. Check that the entry points to Microsoft's project.
2. Right-click the server and choose **Install in Workspace**. Start/enable it,
   then enable its **convert_to_markdown** tool in the agent's tool picker.
   For this local PDF, use a server running in your Codespace with access to the
   workspace files; a remote server cannot read your local path automatically.
3. If the gallery entry is unavailable, run this in the terminal:

   ```bash
   cd /workspaces/AI_workshop
   .venv/bin/python -m pip install markitdown-mcp
   ```

   Run **MCP: Add Server** from the Command Palette, choose a command/stdio server,
   enter `/workspaces/AI_workshop/.venv/bin/markitdown-mcp`, and choose **Workspace**.
4. In **Agent** chat, send this prompt (use it instead of the CLI conversion):

   ```text
   Use MarkItDown's convert_to_markdown tool on
   file:///workspaces/AI_workshop/_for_STUDENT/data/notebook4/pipeline_overview_sample.pdf
   Save the returned Markdown unchanged to
   _for_STUDENT/outputs/04_debugging_and_extensions/pipeline_overview_sample.md.
   Create the output folder if needed. Do not rewrite or summarise the tool result.
   ```

[VS Code MCP setup guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

</details>
"""),
        markdown("""
### B · Ask an agent alongside the converter

While conversion runs, create/open **pipeline_overview_sample.agent.md** in the
same output folder. Open **inline chat** in that file and attach the original
PDF if supported. Select a model and send the prompt below. If inline chat cannot
access the PDF or use file tools, use **Agent** mode in the Chat view with the
same prompt. Review and save its edits; if it returns text only, paste it into
this file and save.
"""),
        prompt(AGENT_PROMPT, "PDF to Markdown · Copy into inline chat or Agent chat"),
        markdown("""
### C · Compare side by side

In Explorer, right-click **pipeline_overview_sample.md** → **Select for Compare**;
then right-click **pipeline_overview_sample.agent.md** → **Compare with Selected**.
Keep the original PDF open as your reference.

| Check against the PDF | MarkItDown output | Agent output |
|---|---|---|
| Headings, wording and numbers preserved? | Inspect | Inspect |
| Reading order, tables and diagram labels usable? | Inspect | Inspect |
| Anything missing, duplicated or invented? | Inspect | Inspect |
| Which needs less cleanup for your next task? | Discuss | Discuss |

Note the model selected (or **Auto**), tools actually used, and one concrete
difference. This compares two workflows, not just two models: the agent may use
other extraction tools. Tools can produce similar outputs, and neither result
is automatically better. Choose by faithfulness to the source and downstream
usefulness. Optionally repeat with another model in a fresh chat and a new file.

Some tools and services are free and open source and can be more economical than paid APIs or AI inference providers, especially for tasks that process large volumes of data; consider them alongside their compute and maintenance costs.
"""),
    ]
