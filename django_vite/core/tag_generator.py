from typing import Dict

Tag = str


class TagGenerator:
    @staticmethod
    def script(src: str, attrs: Dict[str, str]) -> Tag:
        """
        Generates an HTML script tag.

        Arguments:
            src {str} -- Source of the script.

        Keyword Arguments:
            attrs {Dict[str, str]} -- List of custom attributes
                for the tag.

        Returns:
            str -- The script tag.
        """

        attrs_str = " ".join([f'{key}="{value}"' for key, value in attrs.items()])

        return f'<script {attrs_str} src="{src}"></script>'

    @staticmethod
    def stylesheet(href: str) -> Tag:
        """
        Generates an HTML <link> stylesheet tag for CSS.

        Arguments:
            href {str} -- CSS file URL.

        Returns:
            str -- CSS link tag.
        """

        return f'<link rel="stylesheet" href="{href}" />'

    @staticmethod
    def stylesheet_preload(href: str) -> Tag:
        """
        Generates an HTML <link> preload tag for CSS.

        Arguments:
            href {str} -- CSS file URL.

        Returns:
            str -- CSS link tag.
        """

        return f'<link rel="preload" href="{href}" as="style" />'

    @staticmethod
    def preload(href: str, attrs: Dict[str, str]) -> Tag:
        attrs_str = " ".join([f'{key}="{value}"' for key, value in attrs.items()])

        return f'<link href="{href}" {attrs_str} />'
