from handlerparent import Handler


class MainPage(Handler):

    """Redirect visitors to the main blog page."""

    def get(self):
        """Redirect visitors to the main blog page."""
        self.redirect("/blog")
