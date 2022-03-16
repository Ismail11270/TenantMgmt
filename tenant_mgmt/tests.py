from re import A
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group
from tenant_mgmt.models import Issue, Property, Address, IssueCategory



class IssuesListTestCase(TestCase):
    def setUp(self) -> None:
        Group.objects.create(name='administrator')
        Group.objects.create(name='manager')
        Group.objects.create(name='employee')
        Group.objects.create(name='tenant')
        return super().setUp()

    def test_list_issues_failed_auth(self):
        c = Client()
        response = c.get("/issues", follow=True)
        chain = response.redirect_chain
        self.assertEqual(chain[0][0], '/issues/')
        self.assertEqual(chain[1][0], '/login/?next=/issues/')
        self.assertEqual(response.status_code, 200)  # login page

    def test_list_issues(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")
        Issue.objects.create(title="test", description="test",
                             submitter=user, related_property=prop)

        response = c.get("/issues/")
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        group = Group.objects.get(name='manager')
        user.groups.add(group)
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")
        category = IssueCategory.objects.create(title="test")
        issue = Issue.objects.create(title="test", description="test",
                                     submitter=user, related_property=prop)

        response = c.post(f"/issues/{issue.id}/edit", {"title":"test2", "description": "test2", "category": category.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Issue.objects.filter(title="test2")), 1)

    def test_create_issue(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        group = Group.objects.get(name='manager')
        user.groups.add(group)
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")
        category = IssueCategory.objects.create(title="test")

        response = c.post(f"/issues/new/", {"title":"test2", "description": "test2", "category": category.id,
                                            "related_property": prop.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Issue.objects.filter(title="test2")), 1)


    def test_delete_issue(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        group = Group.objects.get(name='manager')
        user.groups.add(group)
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")
        issue = Issue.objects.create(title="test", description="test",
                                     submitter=user, related_property=prop)

        response = c.delete(f"/issues/{issue.id}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Issue.objects.filter(title="test")), 0)


class PropertiesListTestCase(TestCase):
    def setUp(self) -> None:
        Group.objects.create(name='administrator')
        Group.objects.create(name='manager')
        Group.objects.create(name='employee')
        Group.objects.create(name='tenant')
        return super().setUp()

    def test_list_property_for_not_manager(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")
        response = c.get("/properties/", follow=True)
        chain = response.redirect_chain
        print(chain)
        self.assertEqual(chain[0][0], '/login/?next=/properties/')
        self.assertEqual(response.status_code, 200)

    def test_list_property(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")

        group = Group.objects.get(name='manager')
        user.groups.add(group)
        response = c.get("/properties/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_property(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")

        group = Group.objects.get(name='manager')
        user.groups.add(group)
        self.assertTrue(Property.objects.all())
        response = c.delete(f"/properties/{prop.id}/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Property.objects.all())


    def test_update_property(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        prop = Property.objects.create(name="test")

        group = Group.objects.get(name='manager')
        user.groups.add(group)
        self.assertTrue(Property.objects.all())

        addr = Address.objects.create(street="test",
                                      apartment="test", city="esse", zipCode='sdf', country='sdf')

        response = c.post(f"/properties/{prop.id}/edit/", {"name":"test2", "address": addr.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Property.objects.filter(name="test2")), 1)

class IssueCategoryTestCase(TestCase):
    def setUp(self) -> None:
        Group.objects.create(name='administrator')
        Group.objects.create(name='manager')
        Group.objects.create(name='employee')
        Group.objects.create(name='tenant')
        return super().setUp()

    def test_category_list(self):
        c = Client()
        user = User.objects.create_user(username='test',
                                        email='test@test.com',
                                        password='testing')
        c.login(username='test', password='testing')
        category = IssueCategory.objects.create(title="test")

        group = Group.objects.get(name='administrator')
        user.groups.add(group)
        response = c.get(f"/categories/")
        self.assertEqual(response.status_code, 200)


