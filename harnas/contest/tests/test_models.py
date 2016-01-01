from django.test import TestCase
from harnas.contest.models import Contest, News, Task, TestEnvironment
from mock import Mock


class ContestTest(TestCase):

    def test_contest_str(self):
        contest = Mock(spec=Contest)
        contest.name = "Test"
        self.assertEqual(Contest.__str__(contest), "Test")


class NewsTest(TestCase):

    def test_news_str(self):
        news = Mock(spec=News)
        news.title = "Test news"
        self.assertEqual(News.__str__(news), "Test news")


class TestEnvironmentTest(TestCase):

    def test_test_environment_str(self):
        env = Mock(spec=TestEnvironment)
        env.template_name = "Test env"
        self.assertEqual(TestEnvironment.__str__(env), "Test env")


class TestTask(TestCase):

    def test_task_str(self):
        task = Mock(spec=Task)
        task.name = "Test task"
        self.assertEqual(Task.__str__(task), "Test task")
