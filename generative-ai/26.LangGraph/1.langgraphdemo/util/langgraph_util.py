from langchain_core.runnables.graph import MermaidDrawMethod
from PIL import Image
from io import BytesIO
from pathlib import Path

def display(runnable, output_file_path=None):
    output_path = Path(output_file_path) if output_file_path else Path.cwd() / "graph.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        graph_image = runnable.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
            output_file_path=str(output_path),
        )
        img = Image.open(BytesIO(graph_image))
        img.show()
        print(f"Graph image saved to: {output_path}")
    except Exception as exc:
        mermaid_path = output_path.with_suffix(".mmd")
        mermaid_path.write_text(runnable.get_graph().draw_mermaid(), encoding="utf-8")
        print(f"Unable to render PNG automatically: {exc}")
        print(f"Mermaid source saved to: {mermaid_path}")
