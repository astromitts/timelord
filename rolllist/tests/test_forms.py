from bs4 import BeautifulSoup

from django.urls import reverse
from project.helpers import TestBaseWithScheduleData
from rolllist.utils import get_relevant_time_id

from rolllist.models.appmodels import (
    ToDoList,
    Note,
    ScheduleItem,
    RecurringScheduleItem
)


class TestScheduleItemForms(TestBaseWithScheduleData):
    def test_add_schedule_item(self):
        """ Verify the add schedule item workflow
        """

        item_data = {
            'title': 'escape',
            'start_time': get_relevant_time_id('8:00 AM'),
            'end_time': get_relevant_time_id('8:30 AM'),
            'location': 'LA'
        }
        self.client.post(
            reverse('add_item', kwargs={'datestr': self.day_url_str, 'start_time_int': get_relevant_time_id('8:00 AM')}),
            item_data
        )
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        self.assertTrue(item_data['title'] in schedule_contents.text)

    def test_edit_schedule_item(self):
        """ Verify the edit schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        item_to_change = schedule_items[1]
        change_data = {
            'title': 'escape',
            'start_time': item_to_change.start_time,
            'end_time': item_to_change.end_time,
            'location': 'LA'
        }
        self.client.post(
            reverse('edit_item', kwargs={'item_id': item_to_change.id, 'recurring': '0'}),
            change_data
        )
        schedule_table = self.client.get(reverse('get_schedule', kwargs={'datestr': self.day_url_str}))
        schedule_contents = BeautifulSoup(schedule_table.content, features='html.parser')
        for item in schedule_items:
            self.assertTrue(change_data['title'] in schedule_contents.text)

    def test_edit_recurring_schedule_item(self):
        """ Verify the edit schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        source_item_to_change = schedule_items.pop()
        item_to_change = source_item_to_change.recurrance
        change_data = {
            'title': 'Change Me',
            'start_time': item_to_change.start_time,
            'end_time': item_to_change.end_time,
            'location': 'NY',
            'recurrance_0': True,
        }
        self.client.post(
            reverse('edit_recurring_item', kwargs={'item_id': item_to_change.id}),
            change_data
        )
        recurring_item = RecurringScheduleItem.objects.get(pk=item_to_change.id)
        self.assertEqual(recurring_item.title, change_data['title'])

    def test_delete_schedule_item(self):
        """ Verify the delete schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()
        item_to_delete = schedule_items[1]
        self.client.post(
            reverse('delete_item_form', kwargs={'item_id': item_to_delete.id, 'recurring': '0'}),
            {
                'item_id': item_to_delete.id
            }
        )
        item_qs = ScheduleItem.objects.filter(id=item_to_delete.id)
        self.assertFalse(item_qs.exists())

    def test_delete_recurring_schedule_item(self):
        """ Verify the delete schedule item workflow
        """
        schedule_items, schedule_dict = self._add_schedule_items()

        item_to_delete = schedule_items.pop()
        self.client.post(
            reverse('delete_item_form', kwargs={'item_id': item_to_delete.id, 'recurring': '1'}),
            {
                'item_id': item_to_delete.id
            }
        )
        item = ScheduleItem.objects.filter(recurrance=item_to_delete.recurrance)
        self.assertFalse(item.exists())


class TestToDoForms(TestBaseWithScheduleData):

    def test_delete_todo_item(self):
        """ Verify the delete view functions for todo items
        """
        todo_items = self._add_todo_items()
        item_to_delete = todo_items[2]

        # note: if the POST data is empty then request.POST resolves to False, so just put {'source': 'test'}
        # in the request to make sure that the code is actually executed
        self.client.post(reverse('delete_todo_item', kwargs={'item_id': item_to_delete.id}), {'source': 'test'})

        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        todo_titles = [element.text for element in todo_content.find_all('span', {'class': 'helper_todoitem--title'})]

        for item in todo_items:
            if item == item_to_delete:
                self.assertFalse(item.title in todo_titles)
            else:
                self.assertTrue(item.title in todo_titles)

    def test_add_todo_item(self):
        """ Verify the delete todo item workflow
        """
        todo_list, created = ToDoList.get_or_create(day=self.day, user=self.user.user.rolllistuser)
        test_title = 'make sure this worrrrrrks'
        self.client.post(
            reverse('add_todo_item', kwargs={'list_id': todo_list.id}),
            {
                'title': test_title,
                'priority': '1'
            }
        )

        todo_response = self.client.get(reverse('get_todo', kwargs={'datestr': self.day_url_str}))
        todo_content = BeautifulSoup(todo_response.content, features='html.parser')
        self.assertTrue(test_title in todo_content.text)


class TestNoteForms(TestBaseWithScheduleData):

    def test_add_note(self):
        self._add_notes()
        init_note_count = Note.objects.all().count()
        test_content = (
            'Sometimes we lose sight of what really matters in life. '
            'There is something to be said for a gourmet brie and '
            'truffle burger paired with parmesan frites, but don\'t '
            'let that make you forget about the ol\' faithful with '
            'American cheddar and a squishy bun.'
        )
        post_view = self.client.post(
            reverse('add_note', kwargs={'datestr': self.day_url_str}),
            {
                'content': test_content
            }
        )
        self.assertEqual(post_view.status_code, 302)
        result_notes = Note.objects.all()
        self.assertEqual(result_notes.count(), init_note_count + 1)
        self.assertTrue(test_content in [n.content for n in result_notes])

    def test_delete_note(self):
        test_notes = self._add_notes()
        init_note_count = Note.objects.all().count()
        note_to_delete = test_notes[0]
        post_view = self.client.post(
            reverse('delete_note', kwargs={'note_id': note_to_delete.id}),
            {'item_id': note_to_delete.id}
        )
        self.assertEqual(post_view.status_code, 200)
        result_notes = Note.objects.all()
        self.assertEqual(result_notes.count(), init_note_count - 1)
        self.assertFalse(note_to_delete in result_notes)

    def test_edit_note(self):
        test_notes = self._add_notes()
        init_note_count = Note.objects.all().count()
        note_to_edit = test_notes[0]
        test_content = (
            'Sometimes we lose sight of what really matters in life. '
            'There is something to be said for a gourmet brie and '
            'truffle burger paired with parmesan frites, but don\'t '
            'let that make you forget about the ol\' faithful with '
            'American cheddar and a squishy bun.'
        )

        post_view = self.client.post(
            reverse('edit_note', kwargs={'note_id': note_to_edit.id}),
            {'content': test_content}
        )
        self.assertEqual(post_view.status_code, 302)
        result_notes = Note.objects.all()
        self.assertEqual(result_notes.count(), init_note_count)
        self.assertTrue(test_content in [n.content for n in result_notes])
