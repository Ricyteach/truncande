import pathlib

import click

from . import candeout


@click.group()
@click.argument("ifile", type=click.Path(exists=True, dir_okay=False), required=True)
@click.argument(
    "ofile",
    type=click.Path(exists=False, dir_okay=False, writable=True),
    required=False,
)
@click.pass_context
def main(ctx, ifile, ofile=""):
    ifile = pathlib.Path(ifile)
    ofile = (
        pathlib.Path(ofile) if ofile else ifile.parent / (ifile.stem + " truncated.txt")
    )
    ctx.ensure_object(dict)
    ctx.obj["ifile"] = ifile
    ctx.obj["ofile"] = ofile
    ctx.obj["candeout"] = candeout.CandeOut(ifile.read_text().split("\n"))


@main.command()
@click.argument("steps", nargs=-1, type=int)
@click.pass_context
def steps(ctx, steps=(-1,)):
    cout: candeout.CandeOut = ctx.obj["candeout"]
    ctx.obj["out"] = candeout.remove_steps(cout, steps)


@main.resultcallback()
@click.pass_context
def write_file(ctx, *args, **kwargs):
    ofile: pathlib.Path = ctx.obj["ofile"]
    ofile.write_text("\n".join(ctx.obj["candeout"].lines))
