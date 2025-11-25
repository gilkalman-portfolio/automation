import csv
import json
import time
import random
import string
import datetime
from playwright.sync_api import Page, expect
import xml.etree.ElementTree as ET
import os


def get_data(node_name, xml_path=None):
    """
    Read specific node value from XML configuration file.

    :param node_name: The XML node name to extract.
    :param xml_path: Optional path to XML file (defaults to configuration/data.xml in project root).
    :return: The text value of the requested node.
    """
    if xml_path is None:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xml_path = os.path.join(base_path, "configuration", "data.xml")

    tree = ET.parse(xml_path)
    root = tree.getroot()
    node = root.find(f".//{node_name}")

    if node is None or node.text is None:
        raise ValueError(f"Node '{node_name}' not found or empty in {xml_path}")

    return node.text.strip()


# ===============================
# Waits (Playwright replacement for Selenium waits)
# ===============================
def wait_for(page: Page, selector: str, wait_type: str = "visible", timeout: int = 10000):
    """
    Generic wait for element in Playwright.
    wait_type: "visible", "attached", "detached", "hidden"
    """
    page.wait_for_selector(selector, state=wait_type, timeout=timeout)


def wait_for_title(page: Page, expected_title: str, timeout: int = 5000):
    """Wait for the page title to match expected title."""
    expect(page).to_have_title(expected_title, timeout=timeout)


def wait_for_count(page: Page, selector: str, expected_count: int, timeout: int = 10000):
    """Wait until the number of elements that match selector == expected_count."""
    page.wait_for_function(
        f'document.querySelectorAll("{selector}").length === {expected_count}',
        timeout=timeout
    )


# ===============================
# Random Data Generators
# ===============================
def generate_random_username():
    first_names = ["Will", "Keanu", "Katherine", "Tracey", "Oprah", "Myley", "Lady", "Beyonce"]
    last_names = ["Clinton", "DiCaprio", "Trump", "Bush", "Speers", "Cruise", "Swift", "Gates"]
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    separator = random.choice([".", "_", "-"])
    return f"{first_name}{separator}{last_name}"


def generate_random_email(domain="@test.com"):
    username = generate_random_username()
    return f"{username}{domain}"


def generate_random_text(length=30):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_zipcode():
    return f"{random.randint(0, 99999):05d}"


# ===============================
# File Readers
# ===============================
def read_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def read_json(filename):
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


# ===============================
# Utilities
# ===============================
def get_timestamp():
    """Return a formatted timestamp string."""
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_time():
    """Return raw time float."""
    return time.time()
