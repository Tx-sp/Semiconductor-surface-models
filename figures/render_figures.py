import argparse
from io import BytesIO
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from ase.io import read, write
from ase.io.pov import get_bondpairs
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "output"
REPEAT = {"si100": (3, 3, 1), "si111": (3, 3, 1), "inas": (2, 2, 1)}
ROTATIONS = {"top": "", "side": "-90x"}
WIDTH_CM = 15.0
DPI = 300
LEGEND_HEIGHT_CM = 0.9
LEGEND_FONT_PT = 10
COLOURS = {"Si": "#FFBE80", "In": "#A675C8", "As": "#5DAA68"}
CAMERA = "orthographic"
BACKGROUND = "White"
TRANSPARENT = False
TEXTURE = "jmol"
RADIUS_SCALE = 0.8
BOND_CUTOFF = 1.1
BOND_WIDTH = 0.08
CELL_WIDTH = 0.04
SHOW_UNIT_CELL = 0
INCLUDE_MACE = False
POVRAY = "povray"

MODELS = {
    "si100": [
        ("si100_p2x1s", "Si100/output/p(2x1)s.traj", "Si100_p2x1s"),
        ("si100_p2x1a", "Si100/output/p(2x1)a.traj", "Si100_p2x1a"),
        ("si100_p2x2", "Si100/output/p(2x2).traj", "Si100_p2x2"),
        ("si100_c4x2", "Si100/output/c(4x2).traj", "Si100_c4x2"),
    ],
    "si111": [
        ("si111_2x1", "Si111/output/(2x1)mp_enhanced_vibrations.traj", "Si111_2x1"),
    ],
    "inas": [
        ("inas_kumpf_c8x2", "InAs/output/c(8x2)_kumpf.traj", "InAs_Kumpf_c8x2"),
        ("inas_miwa_4x2", "InAs/output/miwa_full.traj", "InAs_Miwa_4x2"),
    ],
}


def add_legend(source, destination, symbols):
    with Image.open(source) as image:
        structure = image.convert("RGBA")
    width = structure.width
    height = round(LEGEND_HEIGHT_CM / 2.54 * DPI)
    figure = Figure(figsize=(width / DPI, height / DPI), dpi=DPI)
    FigureCanvasAgg(figure)
    handles = [
        Line2D([], [], marker="o", linestyle="", markersize=7,
               markerfacecolor=colour, markeredgecolor="black",
               markeredgewidth=0.5, label=symbol)
        for symbol, colour in COLOURS.items() if symbol in symbols
    ]
    figure.legend(handles=handles, loc="center", ncol=len(handles),
                  frameon=False, fontsize=max(8, LEGEND_FONT_PT))
    with BytesIO() as buffer:
        figure.savefig(buffer, format="png", dpi=DPI,
                       transparent=TRANSPARENT,
                       facecolor="none" if TRANSPARENT else BACKGROUND)
        buffer.seek(0)
        with Image.open(buffer) as image:
            legend = image.convert("RGBA")
    canvas = Image.new("RGBA", (width, structure.height + height),
                       (255, 255, 255, 0) if TRANSPARENT else BACKGROUND)
    canvas.paste(structure, (0, 0))
    canvas.paste(legend, (0, structure.height))
    canvas.save(destination, dpi=(DPI, DPI))


def render_model(name, path, group, executable):
    atoms = read(path).repeat(REPEAT[group])
    symbols = atoms.get_chemical_symbols()
    colours = [to_rgb(COLOURS[symbol]) for symbol in symbols]
    bonds = get_bondpairs(atoms, radius=BOND_CUTOFF)
    settings = {
        "camera_type": CAMERA,
        "canvas_width": round(WIDTH_CM / 2.54 * DPI),
        "background": BACKGROUND,
        "transparent": TRANSPARENT,
        "textures": [TEXTURE] * len(atoms),
        "bondatoms": bonds,
        "bondlinewidth": BOND_WIDTH,
        "celllinewidth": CELL_WIDTH,
        "display": False,
        "pause": False,
    }
    previous_directory = Path.cwd()
    with TemporaryDirectory(prefix="pov_", dir=OUTPUT) as temporary:
        try:
            os.chdir(temporary)
            render_executable = executable
            if os.name == "nt" and Path(executable).stem.startswith("pvengine"):
                launcher = Path(temporary) / "povray.cmd"
                engine = executable.replace("'", "''")
                launcher.write_text(
                    '@echo off\n'
                    'powershell.exe -NoProfile -Command "'
                    f"$p = Start-Process -FilePath '{engine}' "
                    "-ArgumentList '/EXIT','/NR','/RENDER','%~1' "
                    '-WindowStyle Hidden -Wait -PassThru; exit $p.ExitCode"\n'
                )
                render_executable = str(launcher)
            for view, rotation in ROTATIONS.items():
                renderer = write(f"{name}_{view}.pov", atoms, format="pov",
                                 rotation=rotation, radii=RADIUS_SCALE,
                                 colors=colours, show_unit_cell=SHOW_UNIT_CELL,
                                 povray_settings=settings)
                png = renderer.render(povray_executable=render_executable, stderr=None)
                destination = OUTPUT / f"{name}_{view}.png"
                add_legend(png, destination, symbols)
                print(destination, flush=True)
        finally:
            os.chdir(previous_directory)


def main():
    parser = argparse.ArgumentParser()
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--group", choices=MODELS)
    selection.add_argument("--all", action="store_true")
    versions = parser.add_mutually_exclusive_group()
    versions.add_argument("--include-mace", action="store_true", default=INCLUDE_MACE)
    versions.add_argument("--no-mace", action="store_true")
    versions.add_argument("--mace-only", action="store_true")
    parser.add_argument("--povray", default=POVRAY)
    args = parser.parse_args()
    executable = shutil.which(args.povray)
    if executable is None and os.name == "nt" and args.povray == "povray":
        windows_povray = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "POV-Ray/v3.7/bin/pvengine64.exe"
        if windows_povray.is_file():
            executable = str(windows_povray)
    if executable is None:
        parser.error("POV-Ray not found. Install it on PATH or use --povray PATH.")
    executable = str(Path(executable).resolve())
    jobs = []
    for group in ([args.group] if args.group else MODELS):
        for name, original, mace in MODELS[group]:
            if not args.mace_only:
                jobs.append((name, ROOT / original, group))
            if args.mace_only or (args.include_mace and not args.no_mace):
                jobs.append((name + "_mace", ROOT / "MACE" / mace / "output/mh-1/relaxed.traj", group))
    missing = [str(path) for _, path, _ in jobs if not path.is_file()]
    if missing:
        parser.error("Missing inputs:\n" + "\n".join(missing))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, path, group in jobs:
        render_model(name, path, group, executable)


if __name__ == "__main__":
    main()
