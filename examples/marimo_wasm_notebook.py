# /// script
# requires-python = ">=3.13.7"
# dependencies = [
#     "marimo>=0.20.2",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # CEX parser demo (marimo + WASM)

    If `cite_exchange` is not already available in the runtime, set `wheel_url`
    in the next cell and the notebook will install it with `micropip` when
    running in the browser.
    """)
    return


@app.cell
async def _():
    import importlib
    import importlib.util
    import pathlib
    import sys

    wheel_url = "https://YOUR-HOST/cite_exchange-0.2.0-py3-none-any.whl"

    if importlib.util.find_spec("cite_exchange") is None:
        if sys.platform == "emscripten":
            if "YOUR-HOST" in wheel_url:
                raise ModuleNotFoundError(
                    "cite_exchange is not installed. Set wheel_url to a hosted wheel URL."
                )

            import micropip

            await micropip.install(wheel_url)
        else:
            project_src = pathlib.Path(__file__).resolve().parents[1] / "src"
            sys.path.insert(0, str(project_src))

    importlib.invalidate_caches()

    from cite_exchange import CexBlock, labels

    return CexBlock, labels


@app.cell
def _(mo):
    source = mo.ui.text_area(
        label="CEX source",
        value=(
            "#!ctscatalog\n"
            "urn|citationScheme|groupName|workTitle\n"
            "urn:cts:greekLit:tlg0012.tlg001:|book|Homer|Iliad\n\n"
            "#!ctsdata\n"
            "urn:cts:greekLit:tlg0012.tlg001:1.1|Μῆνιν ἄειδε θεά"
        ),
        full_width=True,
        rows=10,
    )
    label_filter = mo.ui.text(label="Optional label filter", value="")
    return label_filter, source


@app.cell
def _(label_filter, mo, source):
    mo.vstack([source, label_filter])
    return


@app.cell
def _(CexBlock, label_filter, labels, source):
    parsed_labels = labels(source.value)
    selected = label_filter.value.strip() or None
    blocks = CexBlock.from_text(source.value, label=selected)
    summary = [{"label": block.label, "lines": len(block.data)} for block in blocks]
    return blocks, parsed_labels, selected, summary


@app.cell
def _(blocks, mo, parsed_labels, selected, summary):
    heading = (
        f"Found **{len(blocks)}** blocks"
        if not selected
        else f"Found **{len(blocks)}** blocks for label **{selected}**"
    )
    mo.vstack(
        [
            mo.md(heading),
            mo.md("Detected labels: " + ", ".join(parsed_labels) if parsed_labels else "Detected labels: none"),
            mo.ui.table(summary),
        ]
    )
    return


@app.cell
def _(blocks, mo):
    preview = "\n\n".join(block.to_cex() for block in blocks[:2])
    if not preview:
        preview = "(no blocks)"
    mo.md(f"""
    ### Round-trip preview

    ```text
    {preview}
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
