from collections import OrderedDict

time_options_strings = []

time_options_strings.append('12:00 AM')
time_options_strings.append('12:15 AM')
time_options_strings.append('12:30 AM')
time_options_strings.append('12:45 AM')

for i in range(1, 12):
    time_options_strings.append('%s:00 AM' % i)
    time_options_strings.append('%s:15 AM' % i)
    time_options_strings.append('%s:30 AM' % i)
    time_options_strings.append('%s:45 AM' % i)

time_options_strings.append('12:00 PM')
time_options_strings.append('12:15 PM')
time_options_strings.append('12:30 PM')
time_options_strings.append('12:45 PM')

for i in range(1, 12):
    time_options_strings.append('%s:00 PM' % i)
    time_options_strings.append('%s:15 PM' % i)
    time_options_strings.append('%s:30 PM' % i)
    time_options_strings.append('%s:45 PM' % i)

# TODO move this to a user preferences
earliest_time_index = time_options_strings.index('8:00 AM')
latest_time_index = time_options_strings.index('6:30 PM')

relevant_time_dict = {
    i: time_options_strings[i] for i in range(earliest_time_index, latest_time_index + 1)
}

relevant_keys = [i for i in relevant_time_dict.keys()]

weekday_strings = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_strings_abbr = [
    "M", "T", "W", "Th", "F", "Sa", "Su"
]

weekday_display_order = [0, 1, 2, 3, 4, 5, 6]


def _requested_recurrances(data):
    recurrances = []
    for i in range(0, 7):
        field_name = 'recurrance_%s' % i
        if data.get(field_name, 'off') == 'on':
            recurrances.append(i)
    return recurrances


def get_relevant_time_id(search_time):
    for _id, _val in relevant_time_dict.items():
        if _val == search_time:
            return _id


class TimeInterval(object):
    """ Helper object for organizing data about a time interval
    """
    def __init__(self, index, start_string, end_string):
        self.index = index
        self.start_string = start_string
        self.end_string = end_string
        self.items = []
        if index == relevant_keys[-1]:
            self.next_index = None
        else:
            self.next_index = index + 1


class DayScheduleDeux(object):
    """
        [
            (
                item: None,
                intervals: [1, ],
            ),
            (
                item: ScheduleItem(...),
                intervals: [2, ],
            ),
            (
                item: None,
                intervals: [3, ],
            ),
            (
                item: ScheduleItem(...),
                intervals: [3, 4, 5],
            ),
            ...
        ]
    """
    def _organize_by_time(self, scheduled_items):
        return {item.start_time: item for item in scheduled_items}

    def _get_item_intervals(self, item):
        return [i for i in range(item.start_time, item.end_time)]

    def __init__(self, day, user):
        self.day = day
        self.time_intervals = []

        self.scheduled_items = day.get_schedule_items(user)
        items_time_dict = self._organize_by_time(self.scheduled_items)
        self.items_by_time = {i.start_time: i for i in self.scheduled_items}
        self.schedule = []
        used_intervals = []
        self.relevant_time_dict = OrderedDict()
        for i in range(user.schedule_start_time, user.schedule_end_time + 1):
            self.relevant_time_dict[i] = time_options_strings[i]

        self.relevant_keys = [i for i in self.relevant_time_dict.keys()]
        for i, string in self.relevant_time_dict.items():
            # if i not in used_intervals:
            data = {
                'start_time_display': string,
                'intervals': None,
                'item': None,
            }
            if i in items_time_dict:
                data['item'] = items_time_dict[i]

                data['intervals'] = self._get_item_intervals(items_time_dict[i])
                used_intervals += data['intervals']
            data['interval'] = i
            self.schedule.append(data)
