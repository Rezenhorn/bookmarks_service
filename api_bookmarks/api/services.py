import requests
from bs4 import BeautifulSoup
from django.conf import settings
from random_user_agent.params import (
    OperatingSystem,
    SoftwareName,
    SoftwareType
)
from random_user_agent.user_agent import UserAgent

from .exceptions import BadResponse, EmptyTagsError, NoHtmlProvided


def get_request_headers() -> dict[str, str]:
    """Возвращает заголовки запроса со случайным user-agent."""
    user_agent_rotator = UserAgent(
        software_names=[SoftwareName.CHROME.value],
        operating_systems=[OperatingSystem.WINDOWS.value],
        software_types=[SoftwareType.WEB_BROWSER.value],
        limit=100,
    )
    user_agent = user_agent_rotator.get_random_user_agent()
    return {
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-agent': user_agent,
        'Accept-Encoding': 'gzip, deflate',
        'Content-Encoding': 'gzip',
    }


def _get_website_soup(url: str) -> BeautifulSoup:
    """Возвращает объект `BeautifulSoup` страницы."""
    response = requests.get(
        url,
        headers=get_request_headers(),
        timeout=settings.REQUEST_TIMEOUT_S
    )
    if not response.ok:
        raise BadResponse(f"Статус-код ответа: {response.status_code}")
    if not response.content:
        raise NoHtmlProvided
    return BeautifulSoup(response.content, features='html.parser')


def _parse_tag(soup: BeautifulSoup, tag: str) -> str:
    """Возвращает содержание тега Open graph."""
    elem = soup.find('meta', {'property': f'og:{tag}'})
    if not elem or not elem.get('content'):
        return None
    return elem['content']


def _parse_title(soup: BeautifulSoup) -> str:
    """Возвращает содержание тега title."""
    return (
        soup.title.string
        if soup.title and soup.title.string
        else ''
    )


def _parse_meta_description(soup: BeautifulSoup) -> str | None:
    """Возвращает содержание тега meta description."""
    if metatag := soup.find('meta', {'name': 'description'}):
        return metatag.get('content')
    return None


def parse_tags(
    url: str, parse_tags: list[str] = settings.PARSE_TAGS
) -> dict[str, str]:
    """
    Возвращает словарь с Open graph тегами страницы.
    В случае, если их нет, возвращает информацию из тегов
    title и meta description.
    """
    soup = _get_website_soup(url)
    parsed_data = {}
    for tag in parse_tags:
        tag_data = _parse_tag(soup, tag)
        if tag_data:
            parsed_data[tag] = _parse_tag(soup, tag)
    if not parsed_data:
        if title := _parse_title(soup):
            parsed_data['title'] = title
        if description := _parse_meta_description(soup):
            parsed_data['description'] = description
    if not parsed_data:
        raise EmptyTagsError
    return parsed_data
