import os

from RPA.Robocorp.WorkItems import WorkItems

from scraper import NewsScraper

check_robocorp_env_var = os.environ.get("RC_WORKSPACE_ID") is None

if not check_robocorp_env_var:
    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_variables()
    variables = work_item.get("variables", dict())
    search_phrase = variables.get('search_phrase', 'Pakistan')
    months = variables.get('months', 0)
    topics = variables.get('topics', 'california, sports')
else:
    search_phrase = "Pakistan"
    months = 0
    topics = 'Sports'

filter_topics = [topic.strip() for topic in topics.split(',')]
scrapper = NewsScraper(search_phrase=search_phrase, topics=filter_topics, month=months)

scrapper.process()
