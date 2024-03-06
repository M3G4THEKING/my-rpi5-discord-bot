import os
import subprocess
from datetime import datetime

from cogs import CogsExtension
from loggers import setup_package_logger

from .const import TEMPERATURE_COMMAND

logger = setup_package_logger(__name__)


class RaspberryPiUtils(CogsExtension):
    async def get_temperature(self) -> str:
        temperature = float(
            subprocess.check_output(TEMPERATURE_COMMAND, shell=True).decode()
        )

        message = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]: ")

        if temperature > 80:
            self.logger.warning(
                f"Temperature Too High: {temperature} °C, Rebooting")
            self.bot.get_channel(int(os.getenv("TEST_CHANNEL_ID", None))).send(
                f"Temperature Too High: {temperature} °C, Rebooting"
            )
            os.system("sudo reboot")
        elif temperature > 60:
            message += (
                f"Temperature High: {temperature} °C, Consider Rebooting or Cooling"
            )
            self.logger.warning(message)
        else:
            message += f"Temperature: {temperature} °C"
            self.logger.info(message)

        return message
