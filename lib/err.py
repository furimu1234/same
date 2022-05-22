from functools import wraps
from discord.errors import Forbidden, HTTPException, NotFound
from discord.ext.commands import CheckFailure
import traceback, io, discord
from datetime import datetime

__all__ = "excepter"


def excepter(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except NotFound:
            pass
        except Forbidden:
            pass
        except HTTPException:
            pass

        except CheckFailure:
            pass

        except Exception as e:
            print(traceback.format_exc())
            orig_error = getattr(e, "original", e)
            error_msg = "".join(
                traceback.TracebackException.from_exception(orig_error).format()
            )

            with io.StringIO() as f:
                f.write(error_msg)

                channel: discord.TextChannel = self.bot.get_channel(971393539965607946)

                now = datetime.now()
                file_name = now.strftime("%Y年%m月%d日 %H時%M分%S秒")

                await channel.send(file=discord.File(f, filename=f"{file_name}.txt"))

    return wrapped
