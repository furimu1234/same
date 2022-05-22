from discord import Embed, Colour

__all__ = ["succes", "normal", "error"]


def succes(title: str = None, desc: str = None) -> Embed:
    if title is None:
        e = Embed(description=desc, colour=Colour.green())
        return e

    e = Embed(title=title, description=desc, colour=Colour.green())

    return e


def error(desc: str) -> Embed:
    e = Embed(title="Error", description=desc, colour=Colour.magenta())
    return e


def normal(**kwargs) -> Embed:
    e = Embed(
        description=kwargs.get("desc", "")
        if kwargs.get("description") is None
        else kwargs.get("description"),
        colour=Colour.from_rgb(133, 208, 243)
        if kwargs.get("color") is None
        else kwargs.get("color"),
    )

    if title := kwargs.get("title", None):
        e.title = title

    if (url := kwargs.get("url", None)) is not None:
        e.url = url

    return e
